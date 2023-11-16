from typing import Dict, Any
from marketplace.models import Category, Product, CartOrder, CartOrderItems, Wishlist, Address

    
def default(request: Any) -> Dict[str, Any]:
    """
    Retrieves all categories from the database and the address of the current user.
    
    Args:
        request: An object representing the HTTP request made by the user.
        
    Returns:
        A dictionary containing the categories and the user's address.
    """
    categories = Category.objects.all()
    
    return {
        'categories': categories,
    }