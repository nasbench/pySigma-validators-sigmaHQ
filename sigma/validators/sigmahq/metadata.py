from dataclasses import dataclass
from typing import ClassVar, List

from sigma.rule import SigmaRule
from sigma.validators.base import (
    SigmaRuleValidator,
    SigmaValidationIssue,
    SigmaValidationIssueSeverity,
)
from .config import ConfigHQ

config = ConfigHQ()


@dataclass
class SigmahqStatusExistenceIssue(SigmaValidationIssue):
    description: ClassVar[str] = "Rule is missing the status field"
    severity: ClassVar[SigmaValidationIssueSeverity] = (
        SigmaValidationIssueSeverity.MEDIUM
    )


class SigmahqStatusExistenceValidator(SigmaRuleValidator):
    """Checks if a rule is missing the status field."""

    def validate(self, rule: SigmaRule) -> List[SigmaValidationIssue]:
        if rule.status is None:
            return [SigmahqStatusExistenceIssue(rule)]
        else:
            return []


@dataclass
class SigmahqStatusIssue(SigmaValidationIssue):
    description: ClassVar[str] = (
        "Rule uses a status field with either Deprecated or Unsupported values, and it is not located in the appropriate folder."
    )
    severity: ClassVar[SigmaValidationIssueSeverity] = SigmaValidationIssueSeverity.HIGH


class SigmahqStatusValidator(SigmaRuleValidator):
    """Checks if a rule uses a status field with the value Deprecated or Unsupported, and its not located in the appropriate folder."""

    def validate(self, rule: SigmaRule) -> List[SigmaValidationIssue]:
        if rule.status and rule.status.name in ["DEPRECATED", "UNSUPPORTED"]:
            return [SigmahqStatusIssue(rule)]
        else:
            return []


@dataclass
class SigmahqDateExistenceIssue(SigmaValidationIssue):
    description: ClassVar[str] = "Rule is missing the date field"
    severity: ClassVar[SigmaValidationIssueSeverity] = (
        SigmaValidationIssueSeverity.MEDIUM
    )


class SigmahqDateExistenceValidator(SigmaRuleValidator):
    """Checks if a rule is missing the date field."""

    def validate(self, rule: SigmaRule) -> List[SigmaValidationIssue]:
        if rule.date is None:
            return [SigmahqDateExistenceIssue(rule)]
        else:
            return []


@dataclass
class SigmahqDescriptionExistenceIssue(SigmaValidationIssue):
    description: ClassVar[str] = "Rule is missing the description field"
    severity: ClassVar[SigmaValidationIssueSeverity] = (
        SigmaValidationIssueSeverity.MEDIUM
    )


class SigmahqDescriptionExistenceValidator(SigmaRuleValidator):
    """Checks if a rule is missing the description field"""

    def validate(self, rule: SigmaRule) -> List[SigmaValidationIssue]:
        if rule.description is None:
            return [SigmahqDescriptionExistenceIssue(rule)]
        else:
            return []


@dataclass
class SigmahqDescriptionLengthIssue(SigmaValidationIssue):
    description: ClassVar[str] = "Rule has an overly brief description."
    severity: ClassVar[SigmaValidationIssueSeverity] = (
        SigmaValidationIssueSeverity.MEDIUM
    )


class SigmahqDescriptionLengthValidator(SigmaRuleValidator):
    """Checks if a rule has an overly brief description."""

    def validate(self, rule: SigmaRule) -> List[SigmaValidationIssue]:
        if rule.description is not None and len(rule.description) < 16:
            return [SigmahqDescriptionLengthIssue(rule)]
        else:
            return []


@dataclass
class SigmahqLevelExistenceIssue(SigmaValidationIssue):
    description: ClassVar[str] = "Rule is missing the level field"
    severity: ClassVar[SigmaValidationIssueSeverity] = (
        SigmaValidationIssueSeverity.MEDIUM
    )


class SigmahqLevelExistenceValidator(SigmaRuleValidator):
    """Checks if a rule is missing the level field"""

    def validate(self, rule: SigmaRule) -> List[SigmaValidationIssue]:
        if rule.level is None:
            return [SigmahqLevelExistenceIssue([rule])]
        else:
            return []


@dataclass
class SigmahqFalsepositivesCapitalIssue(SigmaValidationIssue):
    description: ClassVar[str] = (
        "Rule contains a falsepositive entry that doesn't start with a capital letter"
    )
    severity: ClassVar[SigmaValidationIssueSeverity] = (
        SigmaValidationIssueSeverity.MEDIUM
    )
    word: str


class SigmahqFalsepositivesCapitalValidator(SigmaRuleValidator):
    """Checks if a rule falsepositive entry starts with a capital letter."""

    def validate(self, rule: SigmaRule) -> List[SigmaValidationIssue]:
        false_positive = []
        if rule.falsepositives:
            for fp in rule.falsepositives:
                if fp[0].upper() != fp[0]:
                    # return only the first word
                    false_positive.append(
                        SigmahqFalsepositivesCapitalIssue(rule, fp.split(" ")[0])
                    )
        return false_positive


@dataclass
class SigmahqFalsepositivesBannedWordIssue(SigmaValidationIssue):
    description: ClassVar[str] = (
        "Rule defines a falsepositive entry that is part of the banned words list"
    )
    severity: ClassVar[SigmaValidationIssueSeverity] = (
        SigmaValidationIssueSeverity.MEDIUM
    )
    word: str


class SigmahqFalsepositivesBannedWordValidator(SigmaRuleValidator):
    """Checks if a rule contains a falsepositive entry that is part of the banned word list."""

    def validate(self, rule: SigmaRule) -> List[SigmaValidationIssue]:
        banned_words = []
        if rule.falsepositives:
            for fp_entry in rule.falsepositives:
                for fp in fp_entry.split(" "):
                    for banned_word in config.sigmahq_fp_banned_word:
                        if fp.lower().strip() == banned_word:
                            banned_words.append(
                                SigmahqFalsepositivesBannedWordIssue(rule, fp)
                            )
        return banned_words


@dataclass
class SigmahqFalsepositivesTypoWordIssue(SigmaValidationIssue):
    description: ClassVar[str] = (
        "Rule contains a falsepositive entry with a common typo."
    )
    severity: ClassVar[SigmaValidationIssueSeverity] = (
        SigmaValidationIssueSeverity.MEDIUM
    )
    word: str


class SigmahqFalsepositivesTypoWordValidator(SigmaRuleValidator):
    """Checks if a rule falsepositive entry contains a common typo."""

    def validate(self, rule: SigmaRule) -> List[SigmaValidationIssue]:
        typos = []
        if rule.falsepositives:
            for fp_entry in rule.falsepositives:
                for fp in fp_entry.split(" "):
                    for typo in config.sigmahq_fp_typo_word:
                        if fp.lower().strip() in typo:
                            typos.append(SigmahqFalsepositivesTypoWordIssue(rule, fp))
        return typos


@dataclass
class SigmahqLinkInDescriptionIssue(SigmaValidationIssue):
    description: ClassVar[str] = (
        "Rule has a description field that contains a reference to a hyperlink. All hyperlinks are reserved for the references field"
    )
    severity: ClassVar[SigmaValidationIssueSeverity] = (
        SigmaValidationIssueSeverity.MEDIUM
    )


class SigmahqLinkInDescriptionValidator(SigmaRuleValidator):
    """Checks if a rule has a description field that contains a reference to a hyperlink."""

    def validate(self, rule: SigmaRule) -> List[SigmaValidationIssue]:
        if rule.description and rule.references == []:
            for link in config.sigmahq_link_in_description:
                if link in rule.description.lower():
                    return [SigmahqLinkInDescriptionIssue(rule)]
        return []


@dataclass
class SigmahqUnknownFieldIssue(SigmaValidationIssue):
    description: ClassVar[str] = "Rule uses an unknown field"
    severity: ClassVar[SigmaValidationIssueSeverity] = (
        SigmaValidationIssueSeverity.MEDIUM
    )
    fieldname: List[str]


class SigmahqUnknownFieldValidator(SigmaRuleValidator):
    """Checks if a rule uses an unknown field."""

    def validate(self, rule: SigmaRule) -> List[SigmaValidationIssue]:
        if len(rule.custom_attributes) > 0:
            return [SigmahqUnknownFieldIssue(rule, list(rule.custom_attributes.keys()))]
        else:
            return []
