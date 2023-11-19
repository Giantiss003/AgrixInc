from typing import Dict, Any
from marketplace.models import Category, Product, Wishlist, Address, Tax
from taggit.models import Tag
    
def default(request: Any) -> Dict[str, Any]:
    """
    Retrieves all categories from the database and the address of the current user.
    
    Args:
        request: An object representing the HTTP request made by the user.
        
    Returns:
        A dictionary containing the categories and the user's address.
    """
    categories = Category.objects.all()
    tags = Tag.objects.all()[:5]
    
    return {
        'categories': categories,
        'tags': tags,
    }
