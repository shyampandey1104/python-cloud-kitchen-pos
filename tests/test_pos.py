"""Unit tests for RestaurantPOSEngine."""

from pos.engine import RestaurantPOSEngine, OrderItem


def test_order_kot_and_settlement():
    engine = RestaurantPOSEngine()
    items = [
        OrderItem(item_name="Dum Biryani", price=320.0, quantity=2, notes="Extra raita"),
        OrderItem(item_name="Paneer Tikka", price=260.0, quantity=1),
    ]

    # Create order & generate KOT
    kots = engine.create_order("ORD-501", items, brand_name="Biryani Box")
    assert len(kots) == 1
    assert kots[0].brand_name == "Biryani Box"
    assert len(kots[0].items) == 2

    # Settle bill with 10% discount
    bill = engine.settle_bill("ORD-501", discount_pct=10.0)
    assert bill["subtotal"] == 900.0  # (320*2 + 260)
    assert bill["discount"] == 90.0
    assert bill["cgst"] == (810.0 * 0.025)
    assert bill["grand_total"] == (810.0 + 810.0 * 0.05)
