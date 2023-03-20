from unittest import TestCase
from src.smalltools_st.behavior.suitable_class_finder import is_concrete, concrete_subclasses, SuitableClassFinder
from .utils import *


class SuitableClassFinderTestCase(TestCase):

    def test_is_concrete(self):
        self.assertFalse(is_concrete(Grandfather))
        self.assertTrue(is_concrete(Aunt))
        self.assertFalse(is_concrete(Uncle))
        self.assertTrue(is_concrete(Cousin))
        self.assertFalse(is_concrete(Father))
        self.assertTrue(is_concrete(Brother))
        self.assertTrue(is_concrete(Sister))
        self.assertTrue(is_concrete(Me))

    def test_concrete_subclasses(self):
        self.assertSetEqual(set(concrete_subclasses(Grandfather, [])), set((Aunt, Cousin, Brother, Sister, Me)))
        self.assertSetEqual(set(concrete_subclasses(Aunt, [])), set())
        self.assertSetEqual(set(concrete_subclasses(Uncle, [])), set((Cousin,)))
        self.assertSetEqual(set(concrete_subclasses(Cousin, [])), set())
        self.assertSetEqual(set(concrete_subclasses(Father, [])), set((Brother, Sister, Me)))
        self.assertSetEqual(set(concrete_subclasses(Brother, [])), set())
        self.assertSetEqual(set(concrete_subclasses(Sister, [])), set())
        self.assertSetEqual(set(concrete_subclasses(Me, [])), set())

    def test_can_handle(self):
        # ONLY concrete subclasses can handle the suitable object
        self.assertEqual(Me, SuitableClassFinder(Relative).suitable_for("John"))
    
        # NO MORE THAN ONE concrete subclass can handle the suitable object
        with self.assertRaises(ValueError):
            SuitableClassFinder(Relative).suitable_for("Jenny")
                
        # JUST ONE concrete subclass should handle the suitable object
        with self.assertRaises(ValueError):
            SuitableClassFinder(Relative).suitable_for("Bob")

    def test_defaultSubclass(self):
        # You can define a default class
        self.assertEqual(Nobody, SuitableClassFinder(Relative).suitable_for("Bob", default_subclass=Nobody))

    def test_suitableMethod(self):
        # You can specify an explicit canHandle method (useful for multiple positional arguments)
        self.assertEqual(Sister, SuitableClassFinder(Relative).suitable_for("Jenny", 14, suitable_method='can_handle_name_and_age'))
