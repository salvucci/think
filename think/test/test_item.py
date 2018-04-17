import unittest
from think import Item, Query, Location, Area


class ItemTest(unittest.TestCase):

    def test_item(self):
        item = Item(slot='val', slot2='val2')
        self.assertEqual('val', item.get('slot'))
        self.assertEqual('val', item.slot)
        self.assertEqual('val2', item.get('slot2'))
        self.assertEqual('val2', item.slot2)

        item = Item().set('slot', 'val').set('slot2', 'val2')
        self.assertEqual('val', item.get('slot'))
        self.assertEqual('val2', item.get('slot2'))

        item.unset('slot2')
        self.assertEqual(None, item.get('slot2'))
        
        item = Item(slot='val', slot2='val2')
        item2 = Item(slot='val', slot2='val2')
        self.assertTrue(item.equals(item))
        self.assertTrue(item2.equals(item2))
        self.assertTrue(item.equals(item2))
        self.assertTrue(item.matches(item))
        self.assertTrue(item2.matches(item2))
        self.assertTrue(item.matches(item2))
        item.unset('slot2')
        self.assertFalse(item.equals(item2))
        self.assertFalse(item.matches(item2))
        self.assertTrue(item2.matches(item))


class QueryTest(unittest.TestCase):

    def test_query(self):
        item = Item(slot='val', slot2='val2')
        self.assertTrue(Query(slot='val').matches(item))
        self.assertTrue(Query().eq('slot', 'val').matches(item))
        self.assertFalse(Query().ne('slot', 'val').matches(item))

        item = Item(slot=3)
        self.assertTrue(Query(slot=3).matches(item))
        self.assertTrue(Query().eq('slot', 3).matches(item))
        self.assertFalse(Query().eq('slot', 2).matches(item))
        self.assertFalse(Query().eq('slot', 4).matches(item))

        self.assertFalse(Query().ne('slot', 3).matches(item))
        self.assertTrue(Query().ne('slot', 2).matches(item))
        self.assertTrue(Query().ne('slot', 4).matches(item))
        
        self.assertFalse(Query().gt('slot', 3).matches(item))
        self.assertTrue(Query().gt('slot', 2).matches(item))
        self.assertFalse(Query().gt('slot', 4).matches(item))

        self.assertFalse(Query().lt('slot', 3).matches(item))
        self.assertFalse(Query().lt('slot', 2).matches(item))
        self.assertTrue(Query().lt('slot', 4).matches(item))

        self.assertTrue(Query().ge('slot', 3).matches(item))
        self.assertTrue(Query().ge('slot', 2).matches(item))
        self.assertFalse(Query().ge('slot', 4).matches(item))

        self.assertTrue(Query().le('slot', 3).matches(item))
        self.assertFalse(Query().le('slot', 2).matches(item))
        self.assertTrue(Query().le('slot', 4).matches(item))


class LocationTest(unittest.TestCase):

    def test_location(self):
        loc = Location(10, 20)
        self.assertEqual('location', loc.isa)
        self.assertEqual(10, loc.x)
        self.assertEqual(20, loc.y)
        loc.move(50, 60)
        self.assertEqual(50, loc.x)
        self.assertEqual(60, loc.y)
        
        loc2 = Location(30, 40, 'loc')
        self.assertEqual('loc', loc2.get('isa'))
        self.assertAlmostEqual(28.28, loc2.distance_to(loc), 2)

        # distance_to_area?
        # angle_to?


class AreaTest(unittest.TestCase):

    def test_area(self):
        area = Area(50, 60, 10, 20)
        self.assertEqual('area', area.isa)
        self.assertEqual(50, area.x)
        self.assertEqual(60, area.y)
        self.assertEqual(10, area.w)
        self.assertEqual(20, area.h)
        self.assertEqual(45, area.x1)
        self.assertEqual(55, area.x2)
        self.assertEqual(50, area.y1)
        self.assertEqual(70, area.y2)

        area.resize(50, 50)
        self.assertEqual(25, area.x1)
        self.assertEqual(75, area.x2)
        self.assertEqual(35, area.y1)
        self.assertEqual(85, area.y2)
        area.resize(10, 20)        

        self.assertTrue(area.contains(Location(50, 60)))
        self.assertTrue(area.contains(Location(45, 50)))
        self.assertTrue(area.contains(Location(55, 70)))
        self.assertFalse(area.contains(Location(44, 50)))
        self.assertFalse(area.contains(Location(56, 70)))
        self.assertFalse(area.contains(Location(45, 49)))
        self.assertFalse(area.contains(Location(55, 71)))

        self.assertAlmostEqual(10, area.approach_width_from(Location(0, 60)), 2)
        self.assertAlmostEqual(20, area.approach_width_from(Location(50, 0)), 2)
