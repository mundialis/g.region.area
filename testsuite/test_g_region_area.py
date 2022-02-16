"""
Name:       g.region.area test
Purpose:    Tests g.region.area inputs.
            Uses NC full sample data set.
Author:     Anika Weinmann and Guido Riembauer
Copyright:  (C) 2020-2022 by mundialis GmbH & Co. KG and the GRASS Development Team
License:    This program is free software; you can redistribute it and/or modify
            it under the terms of the GNU General Public License as published by
            the Free Software Foundation; either version 2 of the License, or
            (at your option) any later version.

            This program is distributed in the hope that it will be useful,
            but WITHOUT ANY WARRANTY; without even the implied warranty of
            MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
            GNU General Public License for more details.
"""

import os

from grass.gunittest.case import TestCase
from grass.gunittest.main import test
from grass.gunittest.gmodules import SimpleModule


class TestGRegionArea(TestCase):
    area_file = "data/area.geojson"
    area_size = 737154516.32
    region_size = 906568009.35
    maximum_small = 600000000
    maximum_high = 1000000000

    pid_str = str(os.getpid())
    area = "area_%s" % pid_str
    region = "region_%s" % pid_str

    @classmethod
    def setUpClass(self):
        """Ensures expected computational region and generated data"""
        # import general area
        self.runModule("v.import", input=self.area_file, output=self.area)
        # set temp region
        self.runModule("g.region", save=self.region)
        # set region to area
        self.runModule("g.region", vector=self.area)

    @classmethod
    def tearDownClass(self):
        """Remove the temporary region and generated data"""
        self.runModule("g.remove", type="vector", name=self.area, flags="f")
        self.runModule("g.region", region=self.region)
        self.runModule("g.remove", type="region", name=self.region, flags="f")

    def test_area_size(self):
        """Test size of area size in map"""
        g_region_area_out = SimpleModule("g.region.area", map=self.area)
        self.assertModule(g_region_area_out)
        # test that error output is not empty
        stderr = g_region_area_out.outputs.stderr
        self.assertTrue(stderr)
        # test that the right map is mentioned in the error message
        self.assertIn("The region has an area of %.2f sqm\n" % self.area_size, stderr)

    def test_area_size_maximum_smaller(self):
        """Test size if area in map is smaller than (small) maximum"""
        g_region_area_out = SimpleModule(
            "g.region.area", map=self.area, maximum=self.maximum_small, flags="t"
        )
        self.assertModule(g_region_area_out)
        # test that error output is not empty
        stderr = g_region_area_out.outputs.stderr
        self.assertTrue(stderr)
        # test that the right map is mentioned in the error message
        self.assertIn(
            "The region has with %.2f sqm a larger area than the given"
            % (self.area_size),
            stderr,
        )
        self.assertIn("maximum (%.2f sqm)\n" % (self.maximum_small), stderr)

    def test_area_size_maximum_smaller_error(self):
        """Test size if area in map is smaller than (small) maximum and throws error"""
        g_region_area_error = SimpleModule(
            "g.region.area", map=self.area, maximum=self.maximum_small
        )
        self.assertModuleFail(g_region_area_error)
        # test that error output is not empty
        stderr = g_region_area_error.outputs.stderr
        self.assertTrue(stderr)
        # test that the right map is mentioned in the error message
        self.assertIn(
            "The region has with %.2f sqm a larger area than the given"
            % (self.area_size),
            stderr,
        )
        self.assertIn("maximum (%.2f sqm)\n" % (self.maximum_small), stderr)

    def test_area_size_maximum_high(self):
        """Test size if area in map is smaller than (high) maximum"""
        g_region_area_out = SimpleModule(
            "g.region.area", map=self.area, maximum=self.maximum_high, flags="t"
        )
        self.assertModule(g_region_area_out)
        # test that error output is not empty
        stderr = g_region_area_out.outputs.stderr
        self.assertTrue(stderr)
        # test that the right map is mentioned in the error message
        self.assertIn(
            "The region has with %.2f sqm a smaller area than the given maximum"
            % (self.area_size),
            stderr,
        )
        self.assertIn("(%.2f sqm)" % (self.maximum_high), stderr)

    def test_area_size_maximum_high_error(self):
        """Test size if area in map is smaller than (high) maximum and does
        not throw error"""
        g_region_area_out = SimpleModule(
            "g.region.area", map=self.area, maximum=self.maximum_high
        )
        self.assertModule(g_region_area_out)
        # test that error output is not empty
        stderr = g_region_area_out.outputs.stderr
        self.assertTrue(stderr)
        # test that the right map is mentioned in the error message
        self.assertIn(
            "The region has with %.2f sqm a smaller area than the given maximum"
            % (self.area_size),
            stderr,
        )
        self.assertIn("(%.2f sqm)" % (self.maximum_high), stderr)

    def test_region_size(self):
        """Test size of the region size"""
        g_region_area_out = SimpleModule("g.region.area")
        self.assertModule(g_region_area_out)
        # test that error output is not empty
        stderr = g_region_area_out.outputs.stderr
        self.assertTrue(stderr)
        # test that the right map is mentioned in the error message
        self.assertIn("The region has an area of %.2f sqm\n" % self.region_size, stderr)

    def test_region_size_maximum_smaller(self):
        """Test size if the region is larger than (small) maximum"""
        g_region_area_out = SimpleModule(
            "g.region.area", maximum=self.maximum_small, flags="t"
        )
        self.assertModule(g_region_area_out)
        # test that error output is not empty
        stderr = g_region_area_out.outputs.stderr
        self.assertTrue(stderr)
        # test that the right map is mentioned in the error message
        self.assertIn(
            "The region has with %.2f sqm a larger area than the given"
            % (self.region_size),
            stderr,
        )
        self.assertIn("maximum (%.2f sqm)\n" % (self.maximum_small), stderr)

    def test_region_size_maximum_smaller_error(self):
        """Test size if the region is larger than (small) maximum and throws error"""
        g_region_area_error = SimpleModule("g.region.area", maximum=self.maximum_small)
        self.assertModuleFail(g_region_area_error)
        # test that error output is not empty
        stderr = g_region_area_error.outputs.stderr
        self.assertTrue(stderr)
        # test that the right map is mentioned in the error message
        self.assertIn(
            "The region has with %.2f sqm a larger area than the given"
            % (self.region_size),
            stderr,
        )
        self.assertIn("maximum (%.2f sqm)\n" % (self.maximum_small), stderr)

    def test_region_size_maximum_high(self):
        """Test size if the region is smaller than (high) maximum"""
        g_region_area_out = SimpleModule(
            "g.region.area", maximum=self.maximum_high, flags="t"
        )
        self.assertModule(g_region_area_out)
        # test that error output is not empty
        stderr = g_region_area_out.outputs.stderr
        self.assertTrue(stderr)
        # test that the right map is mentioned in the error message
        self.assertIn(
            "The region has with %.2f sqm a smaller area than the given maximum"
            % (self.region_size),
            stderr,
        )
        self.assertIn("(%.2f sqm)" % (self.maximum_high), stderr)

    def test_region_size_maximum_high_error(self):
        """Test size if the region is smaller than (high) maximum"""
        g_region_area_out = SimpleModule("g.region.area", maximum=self.maximum_high)
        self.assertModule(g_region_area_out)
        # test that error output is not empty
        stderr = g_region_area_out.outputs.stderr
        self.assertTrue(stderr)
        # test that the right map is mentioned in the error message
        self.assertIn(
            "The region has with %.2f sqm a smaller area than the given maximum"
            % (self.region_size),
            stderr,
        )
        self.assertIn("(%.2f sqm)" % (self.maximum_high), stderr)


if __name__ == "__main__":
    test()
