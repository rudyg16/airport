# main FastAPI app (app.py)

from fastapi import FastAPI
from routes.flights import router as flights_router
from routes.tickets import router as tickets_router
from routes.passengers import router as passengers_router
from routes.employees import router as employees_router
from routes.airlines import router as airlines_router
from routes.terminals import router as terminals_router
from routes.luggage import router as luggage_router
from routes.users import router as users_router


app = FastAPI()

# Register routes
app.include_router(flights_router, prefix="/flights", tags=["Flights"])
app.include_router(tickets_router, prefix="/tickets", tags=["Tickets"])
app.include_router(passengers_router, prefix="/passengers", tags=["Passengers"])
app.include_router(employees_router, prefix="/employees", tags=["Employees"])
app.include_router(airlines_router, prefix="/airlines", tags=["Airlines"])
app.include_router(terminals_router, prefix="/terminals", tags=["Terminals"])
app.include_router(luggage_router, prefix="/luggage", tags=["Luggage"])
app.include_router(users_router, prefix="/users", tags=["Users"])


