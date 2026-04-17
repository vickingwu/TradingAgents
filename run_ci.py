"""Non-interactive runner for GitHub Actions CI."""
import sys
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def main():
    ticker = os.getenv("TICKER", "NVDA")
    analysis_date = os.getenv("ANALYSIS_DATE", datetime.now().strftime("%Y-%m-%d"))
    llm_provider = os.getenv("LLM_PROVIDER", "openai")
    deep_think_llm = os.getenv("DEEP_THINK_LLM", "gpt-5.4-mini")
    quick_think_llm = os.getenv("QUICK_THINK_LLM", "gpt-5.4-mini")

    from tradingagents.graph.trading_graph import TradingAgentsGraph
    from tradingagents.default_config import DEFAULT_CONFIG

    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = llm_provider
    config["deep_think_llm"] = deep_think_llm
    config["quick_think_llm"] = quick_think_llm
    config["max_debate_rounds"] = 1
    config["max_risk_discuss_rounds"] = 1
    config["data_vendors"] = {
        "core_stock_apis": "yfinance",
        "technical_indicators": "yfinance",
        "fundamental_data": "yfinance",
        "news_data": "yfinance",
    }

    print(f"=== TradingAgents CI Analysis ===")
    print(f"Ticker: {ticker}")
    print(f"Date: {analysis_date}")
    print(f"Provider: {llm_provider}")
    print(f"Deep Think LLM: {deep_think_llm}")
    print(f"Quick Think LLM: {quick_think_llm}")
    print(f"================================\n")

    ta = TradingAgentsGraph(debug=True, config=config)
    _, decision = ta.propagate(ticker, analysis_date)

    print("\n=== FINAL DECISION ===")
    print(decision)
    print("=== END DECISION ===")

if __name__ == "__main__":
    main()
