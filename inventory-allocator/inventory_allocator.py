import copy


class InventoryAllocator:
    @staticmethod
    def get_cheapest_shipments_and_minimize_shipments(order, warehouses):
        shipments = []
        original_order = copy.deepcopy(order)
        num_items_left_to_add_to_shipments = len(order)

        for warehouse in warehouses:
            warehouse_shipment = {
                warehouse.get("name"): {}
            }
            warehouse_shipment_for_entire_order = {
                warehouse.get("name"): {}
            }
            shipment_covers_entire_order = True
            added_items_to_shipment = False
            for item in order:
                if item in warehouse.get("inventory"):
                    if original_order.get(item) < 0:
                        return []
                    elif order.get(item) > 0:
                        quantity_of_item_in_inventory = warehouse.get("inventory").get(item)
                        warehouse_shipment.get(warehouse.get("name"))[item] = quantity_of_item_in_inventory
                        order[item] -= quantity_of_item_in_inventory
                        added_items_to_shipment = True
                        if order.get(item) <= 0:
                            num_items_left_to_add_to_shipments -= 1

                            quantity_to_remove_from_shipment = InventoryAllocator.reduce_shipments_for_item(shipments,
                                                                                                            order,
                                                                                                            item)
                            if quantity_to_remove_from_shipment != -1:
                                order[item] += quantity_to_remove_from_shipment
                                warehouse_shipment.get(warehouse.get("name"))[item] -= quantity_to_remove_from_shipment

                else:
                    shipment_covers_entire_order = False
                    continue

                quantity_of_item_in_inventory = warehouse.get("inventory").get(item)
                if quantity_of_item_in_inventory >= original_order.get(item):
                    warehouse_shipment_for_entire_order[warehouse.get("name")][item] = original_order.get(item)
                else:
                    shipment_covers_entire_order = False

            if shipment_covers_entire_order:
                return [warehouse_shipment_for_entire_order]

            if added_items_to_shipment:
                shipments.append(warehouse_shipment)

        if num_items_left_to_add_to_shipments == 0:
            InventoryAllocator.minimize_shipments(shipments, warehouses)
            return shipments
        return []

    @staticmethod
    def reduce_shipments_for_item(shipments, order, item):
        if order.get(item) < 0:
            quantity_added_to_shipment = 0
            for i in range(len(shipments) - 1, -1, -1):
                shipment = shipments[i]
                warehouse_name = list(shipment.keys())[0]
                shipment_inventory = shipment.get(warehouse_name)
                if item in shipment_inventory:
                    if order.get(item) < 0:
                        if shipment_inventory.get(item) <= abs(order.get(item)):
                            order[item] += shipment_inventory.get(item)
                            shipment[warehouse_name].pop(item)
                            if len(shipment_inventory) == 0:
                                shipments.pop(i)
            if order.get(item) < 0:
                return abs(order.get(item))
        return -1

    @staticmethod
    def minimize_shipments(shipments, warehouses):
        for shipment in shipments:
            warehouse_name = list(shipment.keys())[0]
            potential_shipments = {}
            this_shipment_order = copy.deepcopy(shipment.get(warehouse_name))

            for shipment_to_compare_to in shipments:
                compare_to_warehouse_name = list(shipment_to_compare_to.keys())[0]
                if compare_to_warehouse_name == warehouse_name:
                    continue
                compare_to_warehouse = InventoryAllocator.get_warehouse(warehouses,
                                                                        compare_to_warehouse_name)

                shipment_inventory = shipment.get(warehouse_name)
                shipment_to_compare_to_inventory = shipment_to_compare_to.get(compare_to_warehouse_name)
                compare_to_warehouse_inventory = compare_to_warehouse.get("inventory")

                for item in shipment_inventory:
                    InventoryAllocator.move_item_to_another_shipment(item, this_shipment_order,
                                                                     shipment_inventory, potential_shipments,
                                                                     shipment_to_compare_to_inventory,
                                                                     compare_to_warehouse_inventory,
                                                                     compare_to_warehouse_name)

            can_move_all_items = True
            for quantity in this_shipment_order.values():
                if quantity != 0:
                    can_move_all_items = False
                    break

            if can_move_all_items:
                shipment[warehouse_name] = {}
                for name_of_warehouse in potential_shipments:
                    official_shipment = InventoryAllocator.get_shipment(shipments, name_of_warehouse)
                    official_shipment_inventory = official_shipment.get(name_of_warehouse)
                    potential_shipment_inventory = potential_shipments.get(name_of_warehouse)

                    for item in potential_shipment_inventory:
                        if item in official_shipment_inventory:
                            official_shipment_inventory[item] += potential_shipment_inventory.get(item)
                        else:
                            official_shipment_inventory[item] = potential_shipment_inventory.get(item)

        shipments[:] = [shipment for shipment in shipments if len(shipment.get(list(shipment.keys())[0])) != 0]

        return shipments

    @staticmethod
    def move_item_to_another_shipment(item, this_shipment_order, shipment_inventory, potential_shipments,
                                      shipment_to_compare_to_inventory, compare_to_warehouse_inventory,
                                      compare_to_warehouse_name):
        if item in compare_to_warehouse_inventory and this_shipment_order.get(item) > 0:
            if (item in shipment_to_compare_to_inventory and compare_to_warehouse_inventory.get(
                    item) > shipment_to_compare_to_inventory.get(
                item)) or item not in shipment_to_compare_to_inventory:

                quantity_to_move_to_potential_shipment = 0
                if item not in shipment_to_compare_to_inventory:
                    quantity_to_move_to_potential_shipment = min(
                        compare_to_warehouse_inventory.get(item),
                        shipment_inventory.get(item))
                else:
                    quantity_to_move_to_potential_shipment = min(
                        compare_to_warehouse_inventory.get(item) - shipment_to_compare_to_inventory.get(
                            item), shipment_inventory.get(item))

                this_shipment_order[item] -= quantity_to_move_to_potential_shipment

                if compare_to_warehouse_name not in potential_shipments:
                    potential_shipments[compare_to_warehouse_name] = {
                        item: quantity_to_move_to_potential_shipment}
                elif item in potential_shipments.get(compare_to_warehouse_name):
                    potential_shipments.get(compare_to_warehouse_name)[
                        item] += quantity_to_move_to_potential_shipment
                else:
                    potential_shipments.get(compare_to_warehouse_name)[
                        item] = quantity_to_move_to_potential_shipment

    @staticmethod
    def get_warehouse(warehouses, name):
        for warehouse in warehouses:
            if name == warehouse.get("name"):
                return warehouse
        return None

    @staticmethod
    def get_shipment(shipments, name):
        for shipment in shipments:
            if name in shipment:
                return shipment
        return None
