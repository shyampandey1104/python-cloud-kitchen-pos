"""Cloud Kitchen & Restaurant POS Order Engine in Python."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class OrderItem(BaseModel):
    item_name: str
    price: float
    quantity: int = 1
    notes: Optional[str] = None  # e.g. "Less spicy", "No onion"


class KOT(BaseModel):
    kot_id: str
    order_id: str
    brand_name: str  # e.g. "Biryani Box", "Burger Crave"
    kitchen_station: str  # e.g. Grill, Tandoor, Fryer, Assembly
    items: List[OrderItem]
    status: str = "Queued"  # Queued, Cooking, Ready


class RestaurantPOSEngine:
    """Manages order creation, brand routing, KOT generation, and billing."""

    def __init__(self):
        self.orders: Dict[str, List[OrderItem]] = {}
        self.kots: List[KOT] = []

    def create_order(self, order_id: str, items: List[OrderItem], brand_name: str = "Central Kitchen") -> List[KOT]:
        self.orders[order_id] = items
        kot_id = f"KOT-{order_id}-{len(self.kots) + 1}"
        kot = KOT(
            kot_id=kot_id,
            order_id=order_id,
            brand_name=brand_name,
            kitchen_station="Hot Kitchen",
            items=items,
        )
        self.kots.append(kot)
        return [kot]

    def settle_bill(self, order_id: str, discount_pct: float = 0.0) -> Dict[str, Any]:
        if order_id not in self.orders:
            raise ValueError(f"Order {order_id} not found")

        items = self.orders[order_id]
        subtotal = sum(i.price * i.quantity for i in items)
        discount = subtotal * (discount_pct / 100.0)
        taxable = subtotal - discount

        # Restaurant GST: 2.5% CGST + 2.5% SGST = 5%
        cgst = taxable * 0.025
        sgst = taxable * 0.025
        grand_total = taxable + cgst + sgst

        return {
            "order_id": order_id,
            "items_count": len(items),
            "subtotal": round(subtotal, 2),
            "discount": round(discount, 2),
            "cgst": round(cgst, 2),
            "sgst": round(sgst, 2),
            "grand_total": round(grand_total, 2),
            "status": "Paid",
        }
