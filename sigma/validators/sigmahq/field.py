from pathlib import Path
from dataclasses import dataclass
from typing import ClassVar, Dict, List

from sigma.rule import SigmaRule, SigmaLogSource
from sigma.types import SigmaString
from sigma.validators.base import (
    SigmaValidationIssue,
    SigmaValidationIssueSeverity,
    SigmaDetectionItemValidator,
    SigmaDetectionItem,
)

from sigma.modifiers import (
    SigmaAllModifier,
    SigmaBase64Modifier,
    SigmaBase64OffsetModifier,
    SigmaRegularExpressionDotAllFlagModifier,
    SigmaRegularExpressionFlagModifier,
    SigmaRegularExpressionIgnoreCaseFlagModifier,
    SigmaRegularExpressionModifier,
    SigmaRegularExpressionMultilineFlagModifier,
    SigmaCaseSensitiveModifier,
)
from .config import ConfigHQ

config = ConfigHQ()


@dataclass
class SigmahqSpaceFieldNameIssue(SigmaValidationIssue):
    description: ClassVar[str] = (
        "Rule uses a field name with a space instead of a underscore."
    )
    severity: ClassVar[SigmaValidationIssueSeverity] = SigmaValidationIssueSeverity.HIGH
    field: str


class SigmahqSpaceFieldNameValidator(SigmaDetectionItemValidator):
    """Check if rules uses a field name that contains a space instead of an underscore."""

    def validate_detection_item(
        self, detection_item: SigmaDetectionItem
    ) -> List[SigmaValidationIssue]:
        if detection_item.field and " " in detection_item.field:
            return [SigmahqSpaceFieldNameIssue(self.rule, detection_item.field)]
        else:
            return []


@dataclass
class SigmahqFieldnameCastIssue(SigmaValidationIssue):
    description: ClassVar[str] = "A field name have a cast error"
    severity: ClassVar[SigmaValidationIssueSeverity] = SigmaValidationIssueSeverity.HIGH
    field: str


class SigmahqFieldnameCastValidator(SigmaDetectionItemValidator):
    """Check field name have a cast error."""

    def validate(self, rule: SigmaRule) -> List[SigmaValidationIssue]:
        if rule.logsource in config.sigmahq_logsource_cast:
            self.fields = config.sigmahq_logsource_cast[rule.logsource]
            self.unifields = config.sigmahq_logsource_unicast[rule.logsource]
            return super().validate(rule)
        return []

    def validate_detection_item(
        self, detection_item: SigmaDetectionItem
    ) -> List[SigmaValidationIssue]:
        if (
            detection_item.field is not None
            and detection_item.field.lower() in self.unifields
            and not detection_item.field in self.fields
        ):
            return [SigmahqFieldnameCastIssue(self.rule, detection_item.field)]
        else:
            return []


@dataclass
class SigmahqInvalidFieldnameIssue(SigmaValidationIssue):
    description: ClassVar[str] = "A field name do not exist"
    severity: ClassVar[SigmaValidationIssueSeverity] = SigmaValidationIssueSeverity.HIGH
    field: str


class SigmahqInvalidFieldnameValidator(SigmaDetectionItemValidator):
    """Check field name do not exist in the logsource."""

    def validate(self, rule: SigmaRule) -> List[SigmaValidationIssue]:
        if rule.logsource in config.sigmahq_logsource_cast:
            self.fields = config.sigmahq_logsource_cast[rule.logsource]
            self.unifields = config.sigmahq_logsource_unicast[rule.logsource]
            return super().validate(rule)
        return []

    def validate_detection_item(
        self, detection_item: SigmaDetectionItem
    ) -> List[SigmaValidationIssue]:
        if (
            detection_item.field is not None
            and not detection_item.field.lower() in self.unifields
        ):
            return [SigmahqInvalidFieldnameIssue(self.rule, detection_item.field)]
        else:
            return []


@dataclass
class SigmahqInvalidAllModifierIssue(SigmaValidationIssue):
    description: ClassVar[str] = "All modifier without a list of value"
    severity: ClassVar[SigmaValidationIssueSeverity] = SigmaValidationIssueSeverity.HIGH
    field: str


class SigmahqInvalidAllModifierValidator(SigmaDetectionItemValidator):
    """Check All modifier used with a single value."""

    def validate_detection_item(
        self, detection_item: SigmaDetectionItem
    ) -> List[SigmaValidationIssue]:
        if (
            SigmaAllModifier in detection_item.modifiers
            and len(detection_item.value) < 2
        ):
            return [SigmahqInvalidAllModifierIssue(self.rule, detection_item.field)]
        else:
            return []


@dataclass
class SigmahqFieldDuplicateValueIssue(SigmaValidationIssue):
    description: ClassVar[str] = "Field list value have a dulicate item"
    severity: ClassVar[SigmaValidationIssueSeverity] = SigmaValidationIssueSeverity.HIGH
    field: str
    value: str


class SigmahqFieldDuplicateValueValidator(SigmaDetectionItemValidator):
    """Check uniques value in field list."""

    def validate_detection_item(
        self, detection_item: SigmaDetectionItem
    ) -> List[SigmaValidationIssue]:
        # Special case where value is case sensitive
        if (
            SigmaBase64Modifier in detection_item.modifiers
            or SigmaBase64OffsetModifier in detection_item.modifiers
            or SigmaRegularExpressionDotAllFlagModifier in detection_item.modifiers
            or SigmaRegularExpressionFlagModifier in detection_item.modifiers
            or SigmaRegularExpressionIgnoreCaseFlagModifier in detection_item.modifiers
            or SigmaRegularExpressionModifier in detection_item.modifiers
            or SigmaRegularExpressionMultilineFlagModifier in detection_item.modifiers
            or SigmaCaseSensitiveModifier in detection_item.modifiers
        ):
            value_see = []
            for v in detection_item.value:
                if v in value_see:
                    return [
                        SigmahqFieldDuplicateValueIssue(
                            self.rule, detection_item.field, str(v)
                        )
                    ]
                else:
                    value_see.append(v)
            return []
        else:
            value_see = []
            for v in detection_item.value:
                if str(v).lower() in value_see:
                    return [
                        SigmahqFieldDuplicateValueIssue(
                            self.rule, detection_item.field, str(v)
                        )
                    ]
                else:
                    value_see.append(str(v).lower())
            return []


@dataclass
class SigmahqInvalidAllModifierIssue(SigmaValidationIssue):
    description: ClassVar[str] = "All modifier without a list of value"
    severity: ClassVar[SigmaValidationIssueSeverity] = SigmaValidationIssueSeverity.HIGH
    field: str


class SigmahqInvalidAllModifierValidator(SigmaDetectionItemValidator):
    """Check All modifier used with a single value."""

    def validate_detection_item(
        self, detection_item: SigmaDetectionItem
    ) -> List[SigmaValidationIssue]:
        if (
            SigmaAllModifier in detection_item.modifiers
            and len(detection_item.value) < 2
        ):
            return [SigmahqInvalidAllModifierIssue(self.rule, detection_item.field)]
        else:
            return []


@dataclass
class SigmahqFieldUserIssue(SigmaValidationIssue):
    description: ClassVar[str] = "User Field has a Localized name"
    severity: ClassVar[SigmaValidationIssueSeverity] = SigmaValidationIssueSeverity.HIGH
    field: str
    user: str


class SigmahqFieldUserValidator(SigmaDetectionItemValidator):
    """Check a User field use a localized name."""

    def validate_detection_item(
        self, detection_item: SigmaDetectionItem
    ) -> List[SigmaValidationIssue]:
        # Special case where value is case sensitive
        if (
            detection_item.field
            and "user" in detection_item.field.lower()
            and len(detection_item.value) == 1
        ):
            user = str(detection_item.value[0])
            if "AUTORI" in user or "AUTHORI" in user:
                return [SigmahqFieldUserIssue(self.rule, detection_item.field, user)]
            else:
                return []
        else:
            return []
