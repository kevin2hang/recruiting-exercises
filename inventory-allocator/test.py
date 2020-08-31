import unittest
from inventory_allocator import InventoryAllocator


class Test_Inventory_Allocator(unittest.TestCase):
    def test_case_1(self):
        # Test Case 1: Warehouses do not have enough inventory, should not be shipped
        order1 = {
            "apple": 3,
            "orange": 8
        }
        warehouses1 = [{"name": "owd", "inventory": {"apple": 5, "orange": 6}},
                       {"name": "dm", "inventory": {"apple": 5}}]
        test_case1 = {
            "order": order1,
            "warehouses": warehouses1
        }
        self.assertEqual(InventoryAllocator.get_cheapest_shipments_and_minimize_shipments(order1, warehouses1), [])

    def test_case_2(self):
        # Test Case 2: Shipment can be sent from multiple warehouses but should only ship from one to minimize cost
        order2 = {
            "apple": 5
        }
        warehouses2 = [{"name": "owd", "inventory": {"apple": 5}},
                       {"name": "dm", "inventory": {"apple": 5}}]
        test_case2 = {
            "order": order2,
            "warehouses": warehouses2
        }
        self.assertEqual(InventoryAllocator.get_cheapest_shipments_and_minimize_shipments(order2, warehouses2),
                         [{'owd': {'apple': 5}}])

    def test_case_3(self):
        # Test Case 3: Only one warehouse with just enough inventory to ship, should ship
        order3 = {
            "apple": 1
        }
        warehouses3 = [{"name": "owd", "inventory": {"apple": 1}}]
        test_case3 = {
            "order": order3,
            "warehouses": warehouses3
        }
        self.assertEqual(InventoryAllocator.get_cheapest_shipments_and_minimize_shipments(order3, warehouses3),
                         [{'owd': {'apple': 1}}])

    def test_case_4(self):
        # Test Case 4: Must obtain shipments from many multiple warehouses to satisfy many items in order
        order4 = {
            "apple": 5,
            "orange": 2,
            "peach": 3,
            "banana": 6
        }
        warehouses4 = [{"name": "owd", "inventory": {"apple": 1}},
                       {"name": "wm", "inventory": {"orange": 1}},
                       {"name": "dm", "inventory": {"apple": 5}},
                       {"name": "mw", "inventory": {"apple": 5}},
                       {"name": "dom", "inventory": {"orange": 5, "apple": 3}},
                       {"name": "dow", "inventory": {"apple": 5}},
                       {"name": "wd", "inventory": {"banana": 5}},
                       {"name": "omw", "inventory": {"peach": 2}},
                       {"name": "dw", "inventory": {"apple": 5}},
                       {"name": "dwm", "inventory": {"apple": 5}},
                       {"name": "om", "inventory": {"apple": 5}},
                       {"name": "omd", "inventory": {"apple": 5}},
                       {"name": "wod", "inventory": {"banana": 2}},
                       {"name": "dd", "inventory": {"apple": 5}},
                       {"name": "db", "inventory": {"apple": 5}},
                       {"name": "ddm", "inventory": {"peach": 3}}]
        self.assertEqual(InventoryAllocator.get_cheapest_shipments_and_minimize_shipments(order4, warehouses4),
                         [{'dm': {'apple': 5}}, {'dom': {'orange': 2}}, {'wd': {'banana': 5}}, {'wod': {'banana': 1}},
                          {'ddm': {'peach': 3}}])

    def test_case_5(self):
        # Test Case 5: Similar to test case 4 but with more items and larger quantities, should not ship bc doesn't cover all items
        order5 = {
            "apple": 21,
            "orange": 32,
            "peach": 40,
            "banana": 15,
            "watermelon": 8,
            "lemon": 16
        }
        warehouses5 = [{"name": "owd", "inventory": {"apple": 1, "peach": 4}},
                       {"name": "wm", "inventory": {"orange": 1, "watermelon": 5}},
                       {"name": "dm", "inventory": {"apple": 5, "lemon": 4}},
                       {"name": "mw", "inventory": {"apple": 5, "peach": 3}},
                       {"name": "dom", "inventory": {"orange": 5, "apple": 3}},
                       {"name": "dow", "inventory": {"apple": 5, "watermelon": 4}},
                       {"name": "wd", "inventory": {"banana": 5, "peach": 5}},
                       {"name": "omw", "inventory": {"peach": 2, "watermelon": 10}},
                       {"name": "dw", "inventory": {"apple": 5, "lemon": 7}},
                       {"name": "dwm", "inventory": {"apple": 5, "peach": 6}},
                       {"name": "om", "inventory": {"apple": 5, "lemon": 8}},
                       {"name": "omd", "inventory": {"apple": 5, "banana": 8}},
                       {"name": "wod", "inventory": {"banana": 2, "orange": 3}},
                       {"name": "dd", "inventory": {"apple": 5, "peach": 10}},
                       {"name": "db", "inventory": {"apple": 5, "orange": 8}},
                       {"name": "ddm", "inventory": {"peach": 3, "orange": 9}}]
        self.assertEqual(InventoryAllocator.get_cheapest_shipments_and_minimize_shipments(order5, warehouses5), [])

    def test_case_6(self):
        # Test Case 6: Should ship only from second warehouse
        # Might want to ship from first & second warehouse as 4, 1
        # but should just ship everything from second warehouse so it is one shipment instead of two
        order6 = {
            "apple": 5
        }
        warehouses6 = [{"name": "owd", "inventory": {"apple": 4}},
                       {"name": "dm", "inventory": {"apple": 5}}]
        self.assertEqual(InventoryAllocator.get_cheapest_shipments_and_minimize_shipments(order6, warehouses6),
                         [{'dm': {'apple': 5}}])

    def test_case_7(self):
        # Test Case 7: can ship from first and second warehouse
        # but should just ship from third warehouse to minimize cost of shipments bc one shimpent is cheaper than multiple shipments
        order7 = {
            "apple": 5
        }
        warehouses7 = [{"name": "owd", "inventory": {"apple": 2}},
                       {"name": "dm", "inventory": {"apple": 3}},
                       {"name": "wm", "inventory": {"apple": 5}}]
        self.assertEqual(InventoryAllocator.get_cheapest_shipments_and_minimize_shipments(order7, warehouses7),
                         [{'wm': {'apple': 5}}])

    def test_case_8(self):
        # Test Case 8: can ship from all warehouses as 2, 2, 3, 1, but should just ship from first two and last warehouse as 2, 2 & 4 to minimize amount of shipments
        order8 = {
            "apple": 8
        }
        warehouses8 = [{"name": "owd", "inventory": {"apple": 2}},
                       {"name": "dm", "inventory": {"apple": 2}},
                       {"name": "wm", "inventory": {"apple": 3}},
                       {"name": "md", "inventory": {"apple": 4}}]
        self.assertEqual(InventoryAllocator.get_cheapest_shipments_and_minimize_shipments(order8,warehouses8), [{'owd': {'apple': 2}}, {'dm': {'apple': 2}}, {'md': {'apple': 4}}])

    def test_case_9(self):
        # Test Case 9: can ship from all inventory but should not to minimize cost
        # If only looking at individual items might say to ship from owd, dm, & md for apple and owd, dm, & wm for peach
        # Should combine these shipments at overlap to minimize amount of shipments
        order9 = {
            "apple": 16,
            "peach": 12
        }
        warehouses9 = [{"name": "owd", "inventory": {"apple": 4, "peach": 2}},
                       {"name": "dm", "inventory": {"apple": 4, "peach": 4}},
                       {"name": "wm", "inventory": {"apple": 6, "peach": 6}},
                       {"name": "md", "inventory": {"apple": 10, "peach": 6}}]
        self.assertEqual(InventoryAllocator.get_cheapest_shipments_and_minimize_shipments(order9,warehouses9), [{'owd': {'peach': 2, 'apple': 4}}, {'dm': {'apple': 4, 'peach': 4}}, {'md': {'apple': 8, 'peach': 6}}])

    def test_case_10(self):
        order10 = {
            "apple": 8,
            "peach": 8
        }
        warehouses10 = [{"name": "owd", "inventory": {"apple": 5, "peach": 1}},
                        {"name": "dm", "inventory": {"apple": 5, "peach": 2}},
                        {"name": "wm", "inventory": {"apple": 3, "peach": 4}},
                        {"name": "md", "inventory": {"apple": 2, "peach": 4}}]
        self.assertEqual(InventoryAllocator.get_cheapest_shipments_and_minimize_shipments(order10,warehouses10), [{'owd': {'apple': 5}}, {'wm': {'peach': 4, 'apple': 3}}, {'md': {'peach': 4}}])

    def test_case_11(self):
        # Test Case 11: Should ship from first & last warehouse to minimize cost
        # If looking only at individual items might say to ship from first two warehouses for apple and first & last warehouse for peach
        order11 = {
            "apple": 6,
            "peach": 9
        }
        warehouses11 = [{"name": "owd", "inventory": {"apple": 1, "peach": 5}},
                        {"name": "dm", "inventory": {"apple": 9, "peach": 1}},
                        {"name": "wm", "inventory": {"apple": 5, "peach": 5}}]
        self.assertEqual(InventoryAllocator.get_cheapest_shipments_and_minimize_shipments(order11,warehouses11), [{'owd': {'peach': 5, 'apple': 1}}, {'wm': {'peach': 4, 'apple': 5}}])

    def test_case_12(self):
        # Test Case 12: Should not ship bc order contains negative amount of items
        order12 = {
            "apple": -5,
            "banana": 4
        }
        warehouses12 = [{"name": "owd", "inventory": {"apple": 4, "banana": 4}},
                        {"name": "dm", "inventory": {"apple": 7, "banana": 3}},
                        {"name": "wm", "inventory": {"apple": 8, "banana": 5}}]
        self.assertEqual(InventoryAllocator.get_cheapest_shipments_and_minimize_shipments(order12, warehouses12), [])

    def test_case_13(self):
        # Test Case 13: Can ship from multiple shipments in beginning, but should ship from only last shipment to minimize cost
        order13 = {
            "apple": 2,
            "orange": 3,
            "peach": 4,
            "banana": 5
        }
        warehouses13 = [{"name": "owd", "inventory": {"apple": 1}},
                        {"name": "wm", "inventory": {"orange": 1}},
                        {"name": "dm", "inventory": {"apple": 5}},
                        {"name": "mw", "inventory": {"apple": 5}},
                        {"name": "dom", "inventory": {"orange": 5, "apple": 3}},
                        {"name": "dow", "inventory": {"apple": 5}},
                        {"name": "wd", "inventory": {"banana": 5}},
                        {"name": "omw", "inventory": {"peach": 2}},
                        {"name": "dw", "inventory": {"apple": 5}},
                        {"name": "dwm", "inventory": {"apple": 5}},
                        {"name": "om", "inventory": {"apple": 5}},
                        {"name": "omd", "inventory": {"apple": 5}},
                        {"name": "wod", "inventory": {"banana": 2}},
                        {"name": "dd", "inventory": {"apple": 5}},
                        {"name": "db", "inventory": {"apple": 5}},
                        {"name": "ddm", "inventory": {"peach": 5, "banana": 5, "apple": 4, "orange": 6}}]
        self.assertEqual(InventoryAllocator.get_cheapest_shipments_and_minimize_shipments(order13, warehouses13), [{'ddm': {'apple': 2, 'orange': 3, 'peach': 4, 'banana': 5}}])

if __name__ == '__main__':
    unittest.main()