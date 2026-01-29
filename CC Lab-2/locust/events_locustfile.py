from locust import HttpUser, task, between, events
from random import randint

class EventsUser(HttpUser):
    """
    Optimized Locust user for /events endpoint
    """

    wait_time = between(1, 3)

    headers = {
        "Accept": "application/json",
        "User-Agent": "LocustLoadTest/2.x"
    }

    def on_start(self):
        # Unique user per simulated client
        self.user_id = f"locust_user_{randint(1000, 9999)}"

    @task(3)
    def view_events(self):
        """
        Frequently executed task
        """
        with self.client.get(
            "/events",
            params={"user": self.user_id},
            headers=self.headers,
            name="/events [GET]",
            catch_response=True
        ) as response:

            if response.status_code != 200:
                response.failure(
                    f"Failed | Status {response.status_code}"
                )
            else:
                response.success()

    @task(1)
    def view_single_event(self):
        """
        Less frequent task
        """
        event_id = randint(1, 100)

        with self.client.get(
            f"/events/{event_id}",
            headers=self.headers,
            name="/events/:id [GET]",
            catch_response=True
        ) as response:

            if response.status_code not in (200, 404):
                response.failure(
                    f"Unexpected status {response.status_code}"
                )
            else:
                response.success()


# ✅ Correct event listener for Locust 2.x+
@events.request.add_listener
def on_request(
    request_type,
    name,
    response_time,
    response_length,
    response,
    context,
    exception,
    **kwargs
):
    if exception:
        print(f"[ERROR] {request_type} {name} | {exception}")
