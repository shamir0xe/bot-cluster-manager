from typing import Dict, List, Optional

from telegram import User
from src.actions.apply_variables import ApplyVariables
from src.models.utility.state_data import StateData
from src.models.page.conditional_proposition import ConditionalProposition
from src.types.operand_types import OperandTypes
from src.types.variable import Variable


class ConditionalPropositionEvaluator:
    @staticmethod
    def eval(
        propositions: List[ConditionalProposition],
        variables: Dict[str, Variable],
        state_data: StateData,
        user: Optional[User],
    ) -> str:
        for proposition in propositions:
            conclusion = ApplyVariables.with_content(
                proposition.con, variables=variables, state_data=state_data, user=user
            )
            if not proposition.hyp:
                return conclusion
            if len(proposition.hyp) != 3:
                raise Exception("Hypothesis should contain exactly 3 parts")
            left_side = ApplyVariables.with_content(
                proposition.hyp[0],
                variables=variables,
                state_data=state_data,
                user=user,
            )
            operand = proposition.hyp[1]
            right_side = ApplyVariables.with_content(
                proposition.hyp[2],
                variables=variables,
                state_data=state_data,
                user=user,
            )
            # print(f"{left_side}{operand}{right_side} ? then {proposition.con}")
            if ConditionalPropositionEvaluator.single_statement(
                left_side, operand, right_side
            ):
                return conclusion

        raise Exception("Invalid porpositions")

    @staticmethod
    def single_statement(l_side, operand, r_side) -> bool:
        if operand == OperandTypes.EQUAL.value:
            return l_side == r_side
        elif operand == OperandTypes.GREATER_EQ.value:
            return l_side >= r_side
        elif operand == OperandTypes.GREATER.value:
            return l_side > r_side
        elif operand == OperandTypes.LESSER.value:
            return l_side < r_side
        elif operand == OperandTypes.LESSER_EQ.value:
            return l_side <= r_side
        elif operand == OperandTypes.NOT_EQUAL.value:
            return l_side != r_side
        return False
