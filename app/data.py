from app.schemas import CompatibilityReport, DeveloperTool, FeatureFlag, RoadmapMilestone, UserProfile

ROADMAP: list[RoadmapMilestone] = [
    RoadmapMilestone(
        year="2025",
        focus="Launch and Global Community Genesis",
        targets=[
            "Layer 0 testnet and pilot XWallet",
            "Whitepaper, tokenomics baseline, and initial DAO framework",
            "Foundational global community expansion campaign",
        ],
    ),
    RoadmapMilestone(
        year="2026",
        focus="Ecosystem Expansion and Real-World Use Cases",
        targets=[
            "No-code chain creation interfaces",
            "Full DAO governance and reputation-driven participation",
            "Community-led Layer 1 ecosystem growth",
        ],
    ),
    RoadmapMilestone(
        year="2027",
        focus="Mainnet Launch and Progressive Decentralization",
        targets=[
            "Layer 0 mainnet launch",
            "AI-assisted collective intelligence workflows for DAO governance",
            "Pilot integrations for public-sector service workflows",
        ],
    ),
    RoadmapMilestone(
        year="2028",
        focus="Global Adoption and Daily Utility",
        targets=[
            "Low-connectivity synchronization pathways",
            "Social + wallet + dApp unified hub experience",
            "Mass-adoption scaling objectives",
        ],
    ),
]

FEATURE_FLAGS: list[FeatureFlag] = [
    FeatureFlag(
        key="socialfi.profile_v2",
        enabled=True,
        rollout_stage="beta",
        description="Reputation scoring and social graph API capabilities.",
    ),
    FeatureFlag(
        key="dao.governance",
        enabled=True,
        rollout_stage="general-availability",
        description="Proposal lifecycle, voting, and delegation API workflows.",
    ),
    FeatureFlag(
        key="wallet.offline_sync",
        enabled=False,
        rollout_stage="planned",
        description="Wallet synchronization support for constrained connectivity environments.",
    ),
]

DEVELOPER_TOOLS: list[DeveloperTool] = [
    DeveloperTool(
        name="No-code chain builder API",
        status="planned",
        description="Provisioning workflows for community-operated Layer 1 networks.",
    ),
    DeveloperTool(
        name="DAO governance SDK",
        status="active",
        description="Programmatic proposal creation, voting, and result retrieval.",
    ),
    DeveloperTool(
        name="Identity and reputation service",
        status="active",
        description="Identity verification, contribution history, and reputation scoring APIs.",
    ),
]

SAMPLE_USERS: list[UserProfile] = [
    UserProfile(wallet_address="0xA0XC001", reputation_score=78.4, country="TR", joined_year=2025),
    UserProfile(wallet_address="0xA0XC002", reputation_score=64.2, country="US", joined_year=2026),
]

COMPATIBILITY = CompatibilityReport(
    network="AOXChain",
    compatible=True,
    supported_standards=["EVM JSON-RPC", "DAO Governance API", "Wallet Sync v1"],
    notes="Roadmap-driven capabilities are enabled progressively by release phase.",
)
