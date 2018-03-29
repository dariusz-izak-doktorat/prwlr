# -*- coding: utf-8 -*-


import unittest
from prowler import *
import pandas as pd
import numpy as np
import subprocess as sp
import json
import pickle


class ApisTest(unittest.TestCase):
    """
    Tests for prowler.apis.
    """
    @classmethod
    def setUpClass(cls):
        """
        Sets up class level attributes for the tests.
        """
        super(ApisTest, cls).setUpClass()
        cls.orgs_ids_out = pd.read_csv("./test_data/test_orgs_ids_out.csv",
                                       sep="\t",
                                       dtype="object")
        cls.org_db_X_ref_out = pd.read_csv("./test_data/test_orgs_db_X_ref.csv",
                                           sep="\t",
                                           names=["ORF_ID",
                                                  "KEGG_ID"],
                                           dtype="object")
        cls.orgs_names = ["Haemophilus influenzae",
                          "Mycoplasma genitalium",
                          "Methanocaldococcus jannaschii",
                          "Synechocystis sp",
                          "Saccharomyces cerevisiae",
                          "Mycoplasma pneumoniae",
                          "Escherichia coli",
                          "Helicobacter pylori",
                          "Methanothermobacter thermautotrophicus",
                          "Bacillus subtilis",
                          "Notus existans"]
        cls.orgs_ids = ["hin",
                        "mge",
                        "mja",
                        "syn",
                        "sce",
                        "mpn",
                        "eco",
                        "hpy",
                        "mth",
                        "bsu"]
        cls.kegg_api = apis.KEGG_API()
        cls.cost_api = apis.Costanzo_API()
        cls.kegg_api.get_organisms_ids("./test_data/test_orgs_ids_in.csv",
                                       skip_dwnld=True)
        cls.kegg_api.get_org_db_X_ref(organism="Saccharomyces cerevisiae",
                                      target_db="orthology",
                                      out_file_name="./test_data/test_orgs_db_X_ref.csv",
                                      skip_dwnld=True)
        '''cls.kegg_api.get_db_entries("./test_data/test_db")
        with open("./test_data/test_db") as fin:
            cls.test_db = fin.read()
        with open("./test_data/test_db_ref") as fin:
            cls.test_db_ref = fin.read()'''

    @classmethod
    # def tearDownClass(cls):
    #     """
    #     Destroys database downloaded during tests.
    #     """
    #     sp.call("rm ./test_data/test_db", shell=True)
    def test_get_organisms_ids(self):
        """
        Test if apis.get_organisms_ids returns correct pandas.DataFrame from
        input csv.
        """
        pd.testing.assert_frame_equal(self.kegg_api.organisms_ids_df,
                                      self.orgs_ids_out)

    def test_org_name_2_kegg_id(self):
        """
        Test if apis.org_name_2_kegg_id returns correct organism ID for
        biological name.
        """
        for org_name, org_id in zip(self.orgs_names, self.orgs_ids):
            self.assertEqual(self.kegg_api.org_name_2_kegg_id(org_name), org_id)

    def test_get_org_db_X_ref(self):
        """
        Test if apis.get_org_db_X_ref returns correct KEGG database
        cross-reference.
        """
        pd.testing.assert_frame_equal(self.kegg_api.org_db_X_ref_df,
                                      self.org_db_X_ref_out)

    '''def test_get_db_entries(self):
        """
        Test if apis.get_db_entries returns correct KEGG database.
        """
        self.assertEqual(self.test_db, self.test_db_ref, "test_db and test_db_ref are not equal.")'''


class DatabasesTests(unittest.TestCase):
    """
    Tests for prowler.databases.
    """
    def setUp(self):
        """
        Sets up class level attributes for the tests.
        """
        self.query_species = ["Haemophilus influenzae",
                              "Mycoplasma genitalium",
                              "Methanocaldococcus jannaschii",
                              "Synechocystis sp",
                              "Saccharomyces cerevisiae",
                              "Mycoplasma pneumoniae",
                              "Escherichia coli",
                              "Helicobacter pylori",
                              "Methanothermobacter thermautotrophicus",
                              "Bacillus subtilis",
                              "Notus existans"]
        self.query_ids = ["hin",
                          "mge",
                          "mja",
                          "syn",
                          "sce",
                          "mpn",
                          "eco",
                          "hpy",
                          "mth",
                          "bsu"]
        self.test_kegg_db_filename = "./test_data/test_kegg_db"
        self.database_type = "Orthology"
        self.organism_name = "Saccharomyces cerevisiae"
        self.IDs = "./test_data/test_orgs_ids_in.csv"
        self.X_ref = "./test_data/test_orgs_db_X_ref.csv"
        self.out_file_name = "./test_data/test_orgs_db_X_ref"
        self.ref_kegg_db = pd.read_pickle("./test_data/ref_kegg_db.pickle")
        with open("./test_data/ref_databases_KEGG_name_ID.pickle", "rb") as fin:
            self.ref_databases_KEGG_name_ID = pickle.load(fin)
        with open("./test_data/ref_databases_KEGG_ID_name.pickle", "rb") as fin:
            self.ref_databases_KEGG_ID_name = pickle.load(fin)
        self.kegg = databases.KEGG(self.database_type)

    def test_parse_database(self):
        """
        Test if KEGG database is properly parsed.
        """
        self.kegg.parse_database(self.test_kegg_db_filename)
        pd.testing.assert_frame_equal(self.kegg.database, self.ref_kegg_db)

    def test_parse_organism_info(self):
        """
        Test if organisms info is properly parsed.
        """
        self.kegg.parse_organism_info(organism=self.organism_name,
                                      reference_species=self.query_species,
                                      IDs=self.IDs,
                                      X_ref=self.X_ref)
        self.assertEqual(self.kegg.name_ID, self.ref_databases_KEGG_name_ID)
        self.assertEqual(self.kegg.ID_name, self.ref_databases_KEGG_ID_name)


class SGA2Test(unittest.TestCase):
    """
    Tests for prowler.databases.SGA2
    """
    def setUp(self):
        """
        Sets up class level attributes for the tests.
        """
        self.sga2 = databases.SGA2()
        self.test_sga_filename = "./test_data/test_sga_v2_1000r.txt"
        self.ref_sga = pd.read_csv("./test_data/ref_sga_v2_1000r.txt")
        self.ref_sga = self.ref_sga.astype({k: v for k, v in self.sga2.dtypes.iteritems()
                                            if k in self.ref_sga.columns})

    def test_parse(self):
        """
        Test if SGA_v2 input file is properly parsed.
        """
        self.sga2.parse(self.test_sga_filename)
        pd.testing.assert_frame_equal(self.ref_sga,
                                      self.sga2.sga)


class AnyNetworkTests(unittest.TestCase):
    """
    Tests for prowler.databases.SGA2
    """
    def setUp(self):
        """
        Sets up class level attributes for the tests.
        """
        self.test_anynwrk_filename = "./test_data/test_anynetwork.xls"
        self.ORF_query_col = "genotype"
        self.ORF_array_col = "target"
        self.sheet_name = "de novo SNPs"
        self.anynwrk = databases.AnyNetwork()
        self.ref_anynwrk = pd.read_pickle("./test_data/ref_anynetwork.pickle")

    def test_parse(self):
        """
        Test if any interaction network in form of xls input file is properly parsed.
        """
        self.anynwrk.parse(self.test_anynwrk_filename,
                           excel=True,
                           sheet_name=self.sheet_name,
                           ORF_query_col=self.ORF_query_col,
                           ORF_array_col=self.ORF_array_col)
        pd.testing.assert_frame_equal(self.ref_anynwrk,
                                      self.anynwrk.sga,
                                      check_dtype=False,
                                      check_names=False)


class ProfileTests(unittest.TestCase):
    """
    Test for prowler.profiles.Profile.
    """
    def setUp(self):
        """
        Sets up class level attributes for the tests.
        """
        self.ref_query = list("acdfhiklostuz")
        self.ref_reference = list("bcefghijklmnprstuwxy")
        self.ref_absent = sorted([i for i in self.ref_query if i not in self.ref_reference])
        self.ref_present = sorted([i for i in self.ref_query if i in self.ref_reference])
        self.alt_pos_sing = "$"
        self.alt_neg_sing = "#"
        self.ref_profile = "-+-+++++-+++-"
        self.ref_alt_profile = "#$#$$$$$#$$$#"
        self.ref_pss = 13
        self.test_profile = profiles.Profile(reference=self.ref_reference,
                                             query=self.ref_query)

    def test__convert(self):
        """
        Test if profile is properly converted.
        """
        self.assertEqual(self.test_profile._convert(positive_sign=self.alt_pos_sing,
                                                    negative_sign=self.alt_neg_sing),
                         list(self.ref_alt_profile))

    def test_isall(self):
        """
        Test if Profile.isall returns True of False properly.
        """
        self.assertTrue(self.test_profile.isall(self.ref_present))
        self.assertFalse(self.test_profile.isall(self.ref_absent))

    def test_isany(self):
        """
        Test if Profile.isany returns True of False properly.
        """
        self.assertTrue(self.test_profile.isany(self.ref_present[:1] +
                                                self.ref_absent))
        self.assertFalse(self.test_profile.isany(self.ref_absent))

    def test_to_string(self):
        """
        Test if profile is properly converted to string.
        """
        self.assertEqual(self.test_profile.to_string(),
                         self.ref_profile)

    def test_to_list(self):
        """
        Test if profile is properly converted to list.
        """
        self.assertEqual(self.test_profile.to_list(),
                         list(self.ref_profile))
        self.assertEqual(self.test_profile.to_list(positive_sign=self.alt_pos_sing,
                                                   negative_sign=self.alt_neg_sing),
                         list(self.ref_alt_profile))

    def test_to_tuple(self):
        """
        Test if profile is properly converted to list.
        """
        self.assertEqual(self.test_profile.to_tuple(),
                         tuple(self.ref_profile))
        self.assertEqual(self.test_profile.to_tuple(positive_sign=self.alt_pos_sing,
                                                    negative_sign=self.alt_neg_sing),
                         tuple(self.ref_alt_profile))

    def test_to_array(self):
        """
        Test if profile is properly converted to numpy.array.
        """
        np.testing.assert_array_equal(self.test_profile.to_array(),
                                      np.array(list(self.ref_profile)))

    def test_to_series(self):
        """
        Test if profile is properly converted to pandas.Series.
        """
        pd.testing.assert_series_equal(self.test_profile.to_series(),
                                       pd.Series(list(self.ref_profile)))

    def test_calculate_pss(self):
        """
        Test if Profiles Similarity Score (PSS) is properly calculated.
        """
        self.assertEqual(self.test_profile.calculate_pss(self.test_profile),
                         self.ref_pss)


class StatsTests(unittest.TestCase):
    """
    Test for prowler.stats.
    """
    def setUp(self):
        """
        Sets up class level attributes for the tests.
        """
        self.profiles_similarity_threshold = 14
        self.p_value = 0.05
        self.GIS_min = 0.04
        self.GIS_max = -0.04
        self.query_species_selector = None
        self.array_species_selector = None
        self.ref_nwrk = pd.read_pickle("./test_data/ref_nwrk.pickle").reset_index(drop=True)
        self.statistics = stats.Stats(self.ref_nwrk, 14)
        self.ref_nwrk_str = pd.read_csv("./test_data/ref_nwrk.csv")
        self.flat_plu = "+" * 16
        self.flat_min = "-" * 16
#        self.ref_nwrk_app = self.ref_nwrk[self.statistics.PROF_Q] = self.ref_nwrk.apply(lambda x: x.to_string())
#        self.ref_nwrk_app = self.ref_nwrk[self.statistics.PROF_A] = self.ref_nwrk.apply(lambda x: x.to_string())

    def test_flat_plu_q(self):
        """
        Test if flat_plu_q selector returns dataframe of same length as
        selection on str.
        """
        pd.testing.assert_series_equal(self.statistics.dataframe[self.statistics.flat_plu_q]
                                       [self.statistics.PROF_Q].apply(lambda x: x.to_string()),
                                       self.ref_nwrk_str[self.ref_nwrk_str[self.statistics.PROF_Q] ==
                                                         self.flat_plu][self.statistics.PROF_Q])

    def test_flat_plu_a(self):
        """
        Test if flat_plu_a selector returns dataframe of same length as
        selection on str.
        """
        pd.testing.assert_series_equal(self.statistics.dataframe[self.statistics.flat_plu_a]
                                       [self.statistics.PROF_A].apply(lambda x: x.to_string()),
                                       self.ref_nwrk_str[self.ref_nwrk_str[self.statistics.PROF_A] ==
                                                         self.flat_plu][self.statistics.PROF_A])

    def test_flat_min_q(self):
        """
        Test if flat_min_q selector returns dataframe of same length as
        selection on str.
        """
        pd.testing.assert_series_equal(self.statistics.dataframe[self.statistics.flat_min_q]
                                       [self.statistics.PROF_Q].apply(lambda x: x.to_string()),
                                       self.ref_nwrk_str[self.ref_nwrk_str[self.statistics.PROF_Q] ==
                                                         self.flat_min][self.statistics.PROF_Q])

    def test_flat_min_a(self):
        """
        Test if flat_min_a selector returns dataframe of same length as
        selection on str.
        """
        pd.testing.assert_series_equal(self.statistics.dataframe[self.statistics.flat_min_a]
                                       [self.statistics.PROF_A].apply(lambda x: x.to_string()),
                                       self.ref_nwrk_str[self.ref_nwrk_str[self.statistics.PROF_A] ==
                                                         self.flat_min][self.statistics.PROF_A])

    def test_no_flat_plu_q(self):
        """
        Test if no_flat_plu_q selector returns dataframe of same length as
        selection on str.
        """
        pd.testing.assert_series_equal(self.statistics.dataframe[self.statistics.no_flat_plu_q]
                                       [self.statistics.PROF_Q].apply(lambda x: x.to_string()),
                                       self.ref_nwrk_str[self.ref_nwrk_str[self.statistics.PROF_Q] !=
                                                         self.flat_plu][self.statistics.PROF_Q])

    def test_no_flat_plu_a(self):
        """
        Test if no_flat_plu_a selector returns dataframe of same length as
        selection on str.
        """
        pd.testing.assert_series_equal(self.statistics.dataframe[self.statistics.no_flat_plu_a]
                                       [self.statistics.PROF_A].apply(lambda x: x.to_string()),
                                       self.ref_nwrk_str[self.ref_nwrk_str[self.statistics.PROF_A] !=
                                                         self.flat_plu][self.statistics.PROF_A])

    def test_no_flat_min_q(self):
        """
        Test if no_flat_min_q selector returns dataframe of same length as
        selection on str.
        """
        pd.testing.assert_series_equal(self.statistics.dataframe[self.statistics.no_flat_min_q]
                                       [self.statistics.PROF_Q].apply(lambda x: x.to_string()),
                                       self.ref_nwrk_str[self.ref_nwrk_str[self.statistics.PROF_Q] !=
                                                         self.flat_min][self.statistics.PROF_Q])

    def test_no_flat_min_a(self):
        """
        Test if no_flat_min_a selector returns dataframe of same length as
        selection on str.
        """
        pd.testing.assert_series_equal(self.statistics.dataframe[self.statistics.no_flat_min_a]
                                       [self.statistics.PROF_A].apply(lambda x: x.to_string()),
                                       self.ref_nwrk_str[self.ref_nwrk_str[self.statistics.PROF_A] !=
                                                         self.flat_min][self.statistics.PROF_A])


if __name__ == '__main__':
    unittest.main()
