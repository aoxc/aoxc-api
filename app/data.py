from app.schemas import CompatibilityReport, DeveloperTool, FeatureFlag, RoadmapMilestone, UserProfile

ROADMAP: list[RoadmapMilestone] = [
    RoadmapMilestone(
        year="2025",
        focus="Launch & Global Community Genesis",
        targets=[
            "Layer 0 testnet ve test XWallet",
            "Whitepaper, tokenomics ve ilk DAO framework",
            "10 milyon kurucu hareketi",
        ],
    ),
    RoadmapMilestone(
        year="2026",
        focus="Ecosystem Expansion & Real-World Use Cases",
        targets=[
            "No-code blockchain olusturma araclari",
            "Tam DAO yonetimi ve itibar bazli katki",
            "1000+ topluluk odakli Layer 1 zinciri",
        ],
    ),
    RoadmapMilestone(
        year="2027",
        focus="Mainnet Launch & Full Decentralization",
        targets=[
            "Layer 0 Mainnet",
            "AI + DAO kolektif zeka motoru",
            "Kamu hizmetlerinde pilot entegrasyon",
        ],
    ),
    RoadmapMilestone(
        year="2028",
        focus="Global Adoption & Daily Use",
        targets=[
            "Dusuk baglantida offline sync",
            "Sosyal + cuzdan + DApp hub",
            "1 milyar kullanici hedefi",
        ],
    ),
]

FEATURE_FLAGS: list[FeatureFlag] = [
    FeatureFlag(
        key="socialfi.profile_v2",
        enabled=True,
        rollout_stage="beta",
        description="Topluluk itibar skorlamasi ve sosyal graph endpointleri",
    ),
    FeatureFlag(
        key="dao.governance",
        enabled=True,
        rollout_stage="general-availability",
        description="DAO proposal, oylama ve delege endpointleri",
    ),
    FeatureFlag(
        key="wallet.offline_sync",
        enabled=False,
        rollout_stage="planned",
        description="Dusuk baglanti kosullarinda cuzdan esitlemesi",
    ),
]

DEVELOPER_TOOLS: list[DeveloperTool] = [
    DeveloperTool(
        name="No-code chain builder API",
        status="planned",
        description="Topluluklarin kendi Layer1 aglarini API ile olusturmasi",
    ),
    DeveloperTool(
        name="DAO governance SDK",
        status="active",
        description="Teklif olusturma, oy verme ve sonuclari sorgulama",
    ),
    DeveloperTool(
        name="Identity & reputation service",
        status="active",
        description="Kullanici puanlama, kimlik dogrulama ve katkı gecmisi",
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
    notes="Roadmap odakli ozellikler asamali olarak aktiflestirilir.",
)
