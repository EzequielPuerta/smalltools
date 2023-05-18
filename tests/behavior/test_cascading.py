import pytest
from smalltools_st.behavior.cascading import Cascade, Replace, NoReplace
from .utils.cascading import Counter, Repository, BasicCounter

############################################################
# General
############################################################
def test_creation_without_content():
    with pytest.raises(TypeError):
        cascade = Cascade()

def test_creation():
    cascade = Cascade(None)
    assert isinstance(cascade, Cascade)
    assert cascade.yourself is None

def test_cascading_with_attribute_returning_none():
    assert [].append(1) is None
    cascade = Cascade([]).append(1)
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == [1]

def test_cascading_with_attribute_not_returning_none():
    assert [1, 2].pop() == 2
    cascade = Cascade([1, 2]).pop()
    with pytest.raises(AttributeError):
        cascade.yourself
    assert isinstance(cascade, int)
    assert cascade == 2

def test_always_cascading():
    assert [1, 2].pop() == 2
    cascade = Cascade([1, 2], always=True).pop()
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == [1]

def test_replace_strategy():
    assert [1, 2].pop() == 2
    cascade = Cascade([1, 2], replace_strategy=Replace).pop()
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == 2

def test_no_replace_strategy():
    assert [1, 2].pop() == 2
    cascade = Cascade([1, 2], replace_strategy=NoReplace).pop()
    assert isinstance(cascade, int)
    assert cascade == 2

############################################################
# Lists
############################################################
def test_list_empty():
    cascade = Cascade([])
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == []

def test_list_with_one_append():
    cascade = Cascade([]).append(1)
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == [1]

def test_list_with_two_appends():
    cascade = Cascade([]).append(1).append(2)
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == [1, 2]

def test_list_with_three_appends():
    cascade = Cascade([]).append(1).append(2).append(3)
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == [1, 2, 3]

def test_list_without_always_cascading_and_attribute_returning_none_keeps_cascading():
    assert [1, 2].reverse() is None
    cascade = Cascade([]).append(1).append(2).append(3).reverse()
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == [3, 2, 1]
    cascade = cascade.append(4)
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == [3, 2, 1, 4]

def test_list_with_always_cascading_and_attribute_returning_none_keeps_cascading():
    assert [1, 2].reverse() is None
    cascade = Cascade([], always=True).append(1).append(2).append(3).reverse()
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == [3, 2, 1]
    cascade = cascade.append(4)
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == [3, 2, 1, 4]

def test_list_without_always_cascading_and_attribute_not_returning_none_doesnt_keep_cascading():
    assert [1, 2].pop() == 2
    cascade = Cascade([]).append(1).append(2).append(3).pop()
    assert isinstance(cascade, int)
    assert cascade == 3
    with pytest.raises(AttributeError):
        cascade.append(4)

def test_list_with_always_cascading_and_attribute_not_returning_none_keeps_cascading():
    assert [1, 2].pop() == 2
    cascade = Cascade([], always=True).append(1).append(2).append(3).pop()
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == [1, 2]
    cascade = cascade.append(4)
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == [1, 2, 4]

############################################################
# Dictionaries
############################################################
def test_dict_empty():
    cascade = Cascade({})
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == {}

def test_dict_with_one_update():
    cascade = Cascade({}).update({1:1})
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == {1:1}

def test_dict_with_two_updates():
    cascade = Cascade({}).update({1:1}).update({2:2})
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == {1:1, 2:2}

def test_dict_with_three_updates():
    cascade = Cascade({}).update({1:1}).update({2:2}).update({3:3})
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == {1:1, 2:2, 3:3}

def test_dict_without_always_cascading_and_attribute_returning_none_keeps_cascading():
    assert {}.clear() is None
    cascade = Cascade({}).update({1:1}).update({2:2}).update({3:3}).clear()
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == {}
    cascade = cascade.update({4:4})
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == {4:4}

def test_dict_with_always_cascading_and_attribute_returning_none_keeps_cascading():
    assert {}.clear() is None
    cascade = Cascade({}, always=True).update({1:1}).update({2:2}).update({3:3}).clear()
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == {}
    cascade = cascade.update({4:4})
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == {4:4}

def test_dict_without_always_cascading_and_attribute_not_returning_none_doesnt_keep_cascading():
    assert {}.keys() is not None
    cascade = Cascade({}).update({1:1}).update({2:2}).update({3:3}).keys()
    assert isinstance(cascade, type({}.keys()))
    assert list(cascade) == [1, 2, 3]
    with pytest.raises(AttributeError):
        cascade.update({4:4})

def test_dict_with_always_cascading_and_attribute_not_returning_none_keeps_cascading():
    assert {}.keys() is not None
    cascade = Cascade({}, always=True).update({1:1}).update({2:2}).update({3:3}).keys()
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == {1:1, 2:2, 3:3}
    cascade = cascade.update({4:4})
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == {1:1, 2:2, 3:3, 4:4}

############################################################
# Sets
############################################################
def test_set_empty():
    cascade = Cascade({})
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == {}

def test_set_with_one_update():
    cascade = Cascade(set()).update([1])
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == {1}

def test_set_with_two_updates():
    cascade = Cascade(set()).update([1]).update([2])
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == {1, 2}

def test_set_with_three_updates():
    cascade = Cascade(set()).update([1]).update([2]).update([3])
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == {1, 2, 3}

def test_set_without_always_cascading_and_attribute_returning_none_keeps_cascading():
    assert {}.clear() is None
    cascade = Cascade(set()).update([1]).update([2]).update([3]).clear()
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == set()
    cascade = cascade.update([4])
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == {4}

def test_set_with_always_cascading_and_attribute_returning_none_keeps_cascading():
    assert {}.clear() is None
    cascade = Cascade(set(), always=True).update([1]).update([2]).update([3]).clear()
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == set()
    cascade = cascade.update([4])
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == {4}

def test_set_without_always_cascading_and_attribute_not_returning_none_doesnt_keep_cascading():
    assert {1, 2, 3}.pop() is not None
    cascade = Cascade(set()).update([1]).update([2]).update([3]).pop()
    assert isinstance(cascade, int)
    assert cascade == 1
    with pytest.raises(AttributeError):
        cascade.update(4)

def test_set_with_always_cascading_and_attribute_not_returning_none_keeps_cascading():
    assert {1, 2, 3}.pop() is not None
    cascade = Cascade(set(), always=True).update([1]).update([2]).update([3]).pop()
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == {2, 3}
    cascade = cascade.update([4])
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == {2, 3, 4}

############################################################
# Tuples
############################################################
def test_tuple_empty():
    cascade = Cascade(())
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == ()

def test_tuple_with_one_add():
    cascade = Cascade(()).__add__((1,))
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == (1,)

def test_tuple_with_two_adds():
    cascade = Cascade(()).__add__((1,)).__add__((2,))
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == (1, 2)

def test_tuple_with_three_adds():
    cascade = Cascade(()).__add__((1,)).__add__((2,)).__add__((3,))
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == (1, 2, 3)

def test_tuple_will_always_use_cascading():
    assert (1, 2, 3).index(2) == 1
    cascade = Cascade(()).__add__((1,)).__add__((2,)).index(2)
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == 1
    cascade = Cascade((), always=True).__add__((1,)).__add__((2,)).index(2)
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == 1

############################################################
# Bool
############################################################
def test_bool():
    cascade = Cascade(True)
    assert isinstance(cascade, Cascade)
    assert cascade.yourself

def test_bool_will_always_use_cascading():
    assert True.__or__(False) == True
    cascade = Cascade(True).__or__(False)
    assert isinstance(cascade, Cascade)
    assert cascade.yourself
    cascade = Cascade(True, always=True).__or__(False)
    assert isinstance(cascade, Cascade)
    assert cascade.yourself

def test_bool_with_many_operations():
    cascade = Cascade(True).__or__(False).__and__(True)
    assert isinstance(cascade, Cascade)
    assert cascade.yourself

############################################################
# Numbers
############################################################
def test_number():
    cascade = Cascade(0)
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == 0

def test_numbers_will_always_use_cascading():
    assert (1).__add__(2) == 3
    cascade = Cascade(1).__add__(2)
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == 3
    cascade = Cascade(1, always=True).__add__(2)
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == 3

def test_numbers_with_many_operations():
    cascade = Cascade(0).__add__(10).__sub__(4).__mul__(2).__truediv__(3)
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == 4

############################################################
# String
############################################################
def test_string_empty():
    cascade = Cascade('')
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == ''

def test_string_will_always_use_cascading():
    cascade = Cascade('').__add__('hello world!')
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == 'hello world!'
    cascade = Cascade('', always=True).__add__('hello world!')
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == 'hello world!'

def test_string_with_many_operations():
    cascade = Cascade('').__add__('  hello world!  ').strip().capitalize()
    assert isinstance(cascade, Cascade)
    assert cascade.yourself == 'Hello world!'

############################################################
# Decorator with value replacement
############################################################
def test_counter_creation():
    counter = Counter(0)
    assert isinstance(counter, Counter)
    assert counter.current_value == 0
    assert str(counter) == '0'
    assert repr(counter) == '0'

def test_counter_add():
    counter = Counter(0).add(1)
    assert isinstance(counter, Counter)
    assert counter.current_value == 1
    assert str(counter) == '1'
    assert repr(counter) == '1'

def test_counter_subtract():
    counter = Counter(0).subtract(1)
    assert isinstance(counter, Counter)
    assert counter.current_value == -1
    assert str(counter) == '-1'
    assert repr(counter) == '-1'

def test_counter_multiply():
    counter = Counter(2).multiply(2)
    assert isinstance(counter, Counter)
    assert counter.current_value == 4
    assert str(counter) == '4'
    assert repr(counter) == '4'

def test_counter_divide():
    counter = Counter(2).divide(2)
    assert isinstance(counter, Counter)
    assert counter.current_value == 1
    assert str(counter) == '1.0'
    assert repr(counter) == '1.0'

def test_multiple_operations_on_counter():
    counter = Counter(0).add(10).subtract(4).multiply(2).divide(3)
    assert isinstance(counter, Counter)
    assert counter.current_value == 4
    assert str(counter) == '4.0'
    assert repr(counter) == '4.0'

def test_counter_is_even():
    counter = Counter(0).add(10).subtract(4).multiply(2).divide(3)
    result = counter.is_even()
    assert isinstance(result, bool)
    assert result

############################################################
# Decorator with value modification
############################################################
def test_empty_repository_creation():
    repo = Repository({})
    assert isinstance(repo, Repository)
    assert repo.content == {}
    assert str(repo) == ''
    assert repr(repo) == ''

def test_repository_with_elements_creation():
    repo = Repository({1:1, 2:2})
    assert isinstance(repo, Repository)
    assert repo.content == {1:1, 2:2}
    assert str(repo) == '* 1 : 1\n* 2 : 2\n'
    assert repr(repo) == '* 1 : 1\n* 2 : 2\n'

def test_repository_add():
    repo = Repository({}).add(1, 1)
    assert isinstance(repo, Repository)
    assert repo.content == {1:1}
    assert str(repo) == '* 1 : 1\n'
    assert repr(repo) == '* 1 : 1\n'

def test_repository_remove():
    repo = Repository({1:1}).remove(1)
    assert isinstance(repo, Repository)
    assert repo.content == {}
    assert str(repo) == ''
    assert repr(repo) == ''

def test_multiple_operations_on_repository():
    repo = Repository({}).add(1, 1).add(2, 2).add(3, 3).remove(2)
    assert isinstance(repo, Repository)
    assert repo.content == {1:1, 3:3}
    assert str(repo) == '* 1 : 1\n* 3 : 3\n'
    assert repr(repo) == '* 1 : 1\n* 3 : 3\n'

def test_repository_look_for():
    repo = Repository({}).add(1, 1).add(2, 2).add(3, 3).remove(2)
    result = repo.look_for(1)
    assert isinstance(result, int)
    assert result == 1

############################################################
# Cascade with custom class
############################################################
def test_basic_counter_creation():
    cascade = Cascade(BasicCounter(0))
    assert isinstance(cascade, Cascade)
    assert isinstance(cascade.yourself, BasicCounter)
    assert isinstance(cascade.yourself.current_value, int)
    assert cascade.current_value == 0
    assert str(cascade) == '0'
    assert repr(cascade) == '0'

def test_basic_counter_increment():
    assert BasicCounter(0).increment() is None
    cascade = Cascade(BasicCounter(0)).increment()
    assert isinstance(cascade, Cascade)
    assert isinstance(cascade.yourself, BasicCounter)
    assert isinstance(cascade.yourself.current_value, int)
    assert cascade.current_value == 1
    assert str(cascade) == '1'
    assert repr(cascade) == '1'

def test_basic_counter_decrement():
    assert BasicCounter(0).decrement() is None
    cascade = Cascade(BasicCounter(0)).decrement()
    assert isinstance(cascade, Cascade)
    assert isinstance(cascade.yourself, BasicCounter)
    assert isinstance(cascade.yourself.current_value, int)
    assert cascade.current_value == -1
    assert str(cascade) == '-1'
    assert repr(cascade) == '-1'

def test_multiple_operations_on_basic_counter():
    cascade = Cascade(BasicCounter(0)).increment().decrement().increment().increment()
    assert isinstance(cascade, Cascade)
    assert isinstance(cascade.yourself, BasicCounter)
    assert isinstance(cascade.yourself.current_value, int)
    assert cascade.current_value == 2
    assert str(cascade) == '2'
    assert repr(cascade) == '2'