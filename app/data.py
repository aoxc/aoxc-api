from app.schemas import CompatibilityReport, DeveloperTool, FeatureFlag, RoadmapMilestone, UserProfile

ROADMAP: list[RoadmapMilestone] = [
    RoadmapMilestone(
        year="2025",
        focus="Launch & Global Community Genesis",
        targets=[
            "Layer 0 testnet and XWallet test release",
            "Whitepaper, tokenomics, and first DAO framework",
            "10 million founding movement",
        ],
    ),
    RoadmapMilestone(
        year="2026",
        focus="Ecosystem Expansion & Real-World Use Cases",
        targets=[
            "No-code blockchain creation tools",
            "Full DAO governance and reputation-based contributions",
            "1000+ community-driven Layer 1 chains",
        ],
    ),
    RoadmapMilestone(
        year="2027",
        focus="Mainnet Launch & Full Decentralization",
        targets=[
            "Layer 0 Mainnet",
            "AI + DAO collective intelligence engine",
            "Pilot integrations in public services",
        ],
    ),
    RoadmapMilestone(
        year="2028",
        focus="Global Adoption & Daily Use",
        targets=[
            "Offline sync in low-connectivity environments",
            "Social + wallet + DApp hub",
            "1 billion user target",
        ],
    ),
]

FEATURE_FLAGS: list[FeatureFlag] = [
    FeatureFlag(
        key="socialfi.profile_v2",
        enabled=True,
        rollout_stage="beta",
        description="Community reputation scoring and social graph endpoints",
    ),
    FeatureFlag(
        key="dao.governance",
        enabled=True,
        rollout_stage="general-availability",
        description="DAO proposal, voting, and delegate endpoints",
    ),
    FeatureFlag(
        key="wallet.offline_sync",
        enabled=False,
        rollout_stage="planned",
        description="Wallet synchronization in low-connectivity conditions",
    ),
]

DEVELOPER_TOOLS: list[DeveloperTool] = [
    DeveloperTool(
        name="No-code chain builder API",
        status="planned",
        description="API tooling for communities to build their own Layer 1 networks",
    ),
    DeveloperTool(
        name="DAO governance SDK",
        status="active",
        description="Create proposals, vote, and query governance outcomes",
    ),
    DeveloperTool(
        name="Identity & reputation service",
        status="active",
        description="User scoring, identity verification, and contribution history",
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
    notes="Roadmap-focused features are enabled gradually.",
)
