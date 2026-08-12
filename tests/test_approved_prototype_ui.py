from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "static/index.html").read_text(encoding="utf-8")
JS = (ROOT / "static/community.js").read_text(encoding="utf-8")
CSS = (ROOT / "static/community-prototype.css").read_text(encoding="utf-8")


def test_approved_home_information_hierarchy_is_present():
    required = [
        "Trusted. Timely. Actionable.",
        "Search for anything in your community...",
        "Immediate (Now) — Today",
        "Planning (Next 7 Days) — Plan Ahead",
        "Plan your day better",
        "Discovery (When Needed) — Find & Connect",
        "Authentic Sources",
        "Privacy First",
        "Community First",
        "Post",
        "Messages",
    ]
    for text in required:
        assert text in HTML


def test_governed_apis_remain_the_data_source():
    for endpoint in ["/api/health", "/api/listings", "/api/notices", "/api/events"]:
        assert endpoint in JS
    assert "esc(" in JS


def test_no_prototype_sample_data_is_claimed_as_live():
    forbidden = [
        "Water Supply Restored",
        "Heavy Rain After 5 PM",
        "Bank Holiday",
        "IPL Match",
        "9:30 AM",
        "notificationBadge.textContent='3'",
    ]
    for text in forbidden:
        assert text not in HTML + JS


def test_post_and_messages_remain_truthful_until_backend_exists():
    assert "Resident posting/moderation workflow is not implemented" in JS
    assert "does not provide unrestricted in-app chat" in JS


def test_prototype_styles_are_responsive():
    for selector in [
        ".global-search",
        ".service-shortcuts",
        ".immediate-panel",
        ".planning-panel",
        ".discovery-panel",
        ".community-bottom-nav",
    ]:
        assert selector in CSS
    assert "@media(max-width:560px)" in CSS
