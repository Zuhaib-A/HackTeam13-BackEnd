import azure.functions as func
import json

# Mocked in-memory database for pots
# Replace with Azure Cosmos DB or another real database for production
pots_db = {
    "user1": [{"id": 1, "name": "Groceries", "amount": 500}, {"id": 2, "name": "Rent", "amount": 1000}],
    "user2": [{"id": 3, "name": "Entertainment", "amount": 200}],
    "user3": []
}

# Initialize the Function App
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="get_pots", auth_level=func.AuthLevel.FUNCTION)
def get_pots(req: func.HttpRequest) -> func.HttpResponse:
    """Retrieve all pots for a user."""
    user_id = req.params.get("user_id")
    if not user_id:
        return func.HttpResponse("User ID is required.", status_code=400)

    pots = pots_db.get(user_id, [])
    return func.HttpResponse(json.dumps(pots), mimetype="application/json", status_code=200)


@app.route(route="create_pot", auth_level=func.AuthLevel.FUNCTION)
def create_pot(req: func.HttpRequest) -> func.HttpResponse:
    """Create a new pot."""
    user_id = req.params.get("user_id")
    if not user_id:
        return func.HttpResponse("User ID is required.", status_code=400)

    try:
        pot_data = req.get_json()
        if not pot_data.get("name") or not pot_data.get("amount"):
            return func.HttpResponse("Pot name and amount are required.", status_code=400)

        new_pot = {
            "id": len(pots_db.get(user_id, [])) + 1,
            "name": pot_data["name"],
            "amount": pot_data["amount"]
        }
        pots_db.setdefault(user_id, []).append(new_pot)
        return func.HttpResponse(json.dumps(new_pot), mimetype="application/json", status_code=201)
    except ValueError:
        return func.HttpResponse("Invalid JSON data.", status_code=400)


@app.route(route="update_pot", auth_level=func.AuthLevel.FUNCTION)
def update_pot(req: func.HttpRequest) -> func.HttpResponse:
    """Update an existing pot."""
    user_id = req.params.get("user_id")
    pot_id = req.params.get("pot_id")
    if not user_id or not pot_id:
        return func.HttpResponse("User ID and Pot ID are required.", status_code=400)

    try:
        pot_data = req.get_json()
        if not pot_data.get("name") and not pot_data.get("amount"):
            return func.HttpResponse("Pot name or amount must be provided.", status_code=400)

        pots = pots_db.get(user_id, [])
        for pot in pots:
            if pot["id"] == int(pot_id):
                if "name" in pot_data:
                    pot["name"] = pot_data["name"]
                if "amount" in pot_data:
                    pot["amount"] = pot_data["amount"]
                return func.HttpResponse(json.dumps(pot), mimetype="application/json", status_code=200)

        return func.HttpResponse("Pot not found.", status_code=404)
    except ValueError:
        return func.HttpResponse("Invalid JSON data.", status_code=400)


@app.route(route="delete_pot", auth_level=func.AuthLevel.FUNCTION)
def delete_pot(req: func.HttpRequest) -> func.HttpResponse:
    """Delete a pot."""
    user_id = req.params.get("user_id")
    pot_id = req.params.get("pot_id")
    if not user_id or not pot_id:
        return func.HttpResponse("User ID and Pot ID are required.", status_code=400)

    pots = pots_db.get(user_id, [])
    for pot in pots:
        if pot["id"] == int(pot_id):
            pots.remove(pot)
            return func.HttpResponse(f"Pot {pot_id} deleted successfully.", status_code=200)

    return func.HttpResponse("Pot not found.", status_code=404)


@app.route(route="suggest_pots", auth_level=func.AuthLevel.FUNCTION)
def suggest_pots(req: func.HttpRequest) -> func.HttpResponse:
    """Suggest pots based on user's spending patterns."""
    user_id = req.params.get("user_id")
    if not user_id:
        return func.HttpResponse("User ID is required.", status_code=400)

    # Simulate AI-based suggestions
    suggestions = [
        {"name": "Savings", "amount": 300, "predicted_savings": 50},
        {"name": "Utilities", "amount": 150, "predicted_savings": 20}
    ]
    return func.HttpResponse(json.dumps(suggestions), mimetype="application/json", status_code=200)
