import unittest
import foil_gen



new_app = foil_gen.Application()


class TestFoilGen(unittest.TestCase):
	"""
	In foil_gen file, comment out the last lines.
	These start the TKinter app and interfere with unittest.
	"""


	def test_last_rough_cut1(self):
		# reveals the problem at assertion for total_cut_area
		new_app.section_width_var.set(8)
		new_app.section_thickness_var.set(1)
		new_app.regime_split_var.set(.95)
		new_app.facet_tolerance_var.set(0.35)
		new_app.max_chine_length_var.set(0.25)

		new_app.drawFoilChined()

		new_app.max_cut_area_var.set(40)
		new_app.stock_width_var.set(8.1)
		new_app.stock_thickness_var.set(1.2)
		new_app.bit_diameter_var.set(11.35)

		new_app.drawRoughCut()


	def test_last_rough_cut2(self):
		# problem at assertion for total_cut_area goes away with sufficient stock
		new_app.section_width_var.set(8)
		new_app.section_thickness_var.set(1)
		new_app.regime_split_var.set(.95)
		new_app.facet_tolerance_var.set(0.35)
		new_app.max_chine_length_var.set(0.25)

		new_app.drawFoilChined()

		new_app.max_cut_area_var.set(40)
		new_app.stock_width_var.set(8.5)
		new_app.stock_thickness_var.set(1.2)
		new_app.bit_diameter_var.set(11.35)

		new_app.drawRoughCut()


	def test_last_rough_cut3(self):
		# problem at assertion for total_cut_area goes away with small bit
		new_app.section_width_var.set(8)
		new_app.section_thickness_var.set(1)
		new_app.regime_split_var.set(.95)
		new_app.facet_tolerance_var.set(0.35)
		new_app.max_chine_length_var.set(0.25)

		new_app.drawFoilChined()

		new_app.max_cut_area_var.set(40)
		new_app.stock_width_var.set(8.1)
		new_app.stock_thickness_var.set(1.2)
		new_app.bit_diameter_var.set(3.25)

		new_app.drawRoughCut()





if __name__ == "__main__":
    unittest.main()