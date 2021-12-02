from typing import Any, List


class Condition():
    def met(self) -> bool:
        raise NotImplementedError()


class ConditionNot():
    def __init__(self, condition: Condition):
        self.condition = condition

    def met(self) -> bool:
        return not self.condition.met()


class ConditionMultiple(Condition):
    def __init__(self, conditions: List[Condition]):
        self._conditions = conditions


class ConditionMultipleAnd(ConditionMultiple):
    def met(self) -> bool:
        return all(c.met() for c in self._conditions)


class ConditionMultipleOr(ConditionMultiple):
    def met(self) -> bool:
        return any(c.met() for c in self._conditions)


class Action():
    def perform(self):
        raise NotImplementedError()


class Trigger():
    def __init__(self, condition: Condition, action: Action):
        self._condition = condition
        self._action = action

    def trigger(self) -> bool:
        if self._condition.met():
            self._action.perform()
            return True
        return False


class Entity():
    def __init__(self):
        self._properties = {}

    def set_property(self, name: str, value: Any):
        self._properties[name] = value

    def property(self, name: str, default_value: Any = None) -> Any:
        return self._properties.get(name, default_value)


class ConditionEntity(Condition):
    def __init__(self):
        self._entity = None

    def set_entity(self, entity: Entity):
        self._entity = entity


class ConditionEntityProperty(ConditionEntity):
    def __init__(self, property_name: str, value: Any):
        self._property = property_name
        self._value = value


class ConditionEntityPropertyEquals(ConditionEntityProperty):
    def met(self) -> bool:
        return self._entity.property(self._property) == self._value


class ConditionEntityPropertyLessThan(ConditionEntityProperty):
    def met(self) -> bool:
        return self._entity.property(self._property) < self._value


class ActionEntity(Action):
    def __init__(self):
        self._entity = None

    def set_entity(self, entity: Entity):
        self._entity = entity


class ActionEntityPropertySet(ActionEntity):
    def __init__(self, property_name: str, value: Any):
        self._property = property_name
        self._value = value

    def perform(self):
        self._entity.set_property(self._property, self._value)
