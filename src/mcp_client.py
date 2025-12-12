"""MCP Client for calling MCP Finance Calculation Server."""

from mcp import ClientSession  # type: ignore
from mcp.client.streamable_http import streamablehttp_client  # type: ignore
from typing import Dict, List, Union # 딕셔너리 및 타입 힌트 사용을 위해 추가


class MCPFinanceClient:
    """Client to interact with MCP Finance Calculation Server."""

    def __init__(self, mcp_url: str):
        self.mcp_url = mcp_url
        
    def _extract_text_result(self, result):
        """MCP 응답에서 텍스트 내용을 추출하는 내부 도우미 함수."""
        if result.content and len(result.content) > 0:
            content = result.content[0]
            if hasattr(content, 'text'):
                return content.text
        return None


    async def calculate_annual_salary(self, monthly_salary: float, period_months: int = 12) -> str:
        """월급과 기간 기반 연봉 및 예상 월 실수령액을 계산하는 툴을 호출합니다."""
        async with streamablehttp_client(self.mcp_url) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()

                result = await session.call_tool(
                    "calculate_annual_salary",
                    arguments={"monthly_salary": monthly_salary, "period_months": period_months}
                )
                
                # 결과는 딕셔너리 형태의 텍스트 문자열로 반환됩니다.
                content = self._extract_text_result(result)
                if content:
                    return content
                return "연봉 계산 결과를 받지 못했습니다."


    async def calculate_simple_interest(self, principal: float, annual_rate: float, years: float) -> str:
        """저축 원금, 금리, 기간 기반 단순 이자를 계산하는 툴을 호출합니다."""
        async with streamablehttp_client(self.mcp_url) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()

                result = await session.call_tool(
                    "calculate_simple_interest",
                    arguments={"principal": principal, "annual_rate": annual_rate, "years": years}
                )

                # 결과는 딕셔너리 형태의 텍스트 문자열로 반환됩니다.
                content = self._extract_text_result(result)
                if content:
                    return content
                return "이자 계산 결과를 받지 못했습니다."


    async def calculate_loan_repayment(self, principal: float, annual_rate: float, months: int) -> str:
        """대출 원금, 금리, 기간 기반 월 상환액을 계산하는 툴을 호출합니다."""
        async with streamablehttp_client(self.mcp_url) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()

                result = await session.call_tool(
                    "calculate_loan_repayment",
                    arguments={"principal": principal, "annual_rate": annual_rate, "months": months}
                )

                # 결과는 딕셔너리 형태의 텍스트 문자열로 반환됩니다.
                content = self._extract_text_result(result)
                if content:
                    return content
                return "대출 상환액 계산 결과를 받지 못했습니다."


    async def list_tools(self) -> list[dict]:
        """List available tools from MCP server."""
        async with streamablehttp_client(self.mcp_url) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()

                tools = await session.list_tools()
                return [
                    {
                        "name": tool.name,
                        "description": tool.description
                    }
                    for tool in tools.tools
                ]