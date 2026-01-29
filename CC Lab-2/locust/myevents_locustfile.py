from locust import HttpUser, task, between, events
from random import randint
import time

class MyEventsUser(HttpUser):
    """
    Fully optimized Locust user for /my-events endpoint
    """

    # Human-like wait time
    wait_time = between(1, 3)

    # Reusable request headers
    headers = {
        "Accept": "application/json",
        "User-Agent": "LocustLoadTest/2.x"
    }

    def on_start(self):
        """
        Executed once per simulated user
        """
        self.user_id = f"locust_user_{randint(1000, 9999)}"

    @task
    def view_my_events(self):
        """
        Main task: fetch events for a user
        """
        start_time = time.time()

        with self.client.get(
            "/my-events",
            params={"user": self.user_id},
            headers=self.headers,
            name="/my-events [GET]",
            catch_response=True
        ) as response:

            response_time_ms = int((time.time() - start_time) * 1000)

            # Explicit validation
            if response.status_code != 200:
                response.failure(
                    f"Failed | Status: {response.status_code}"
                )
            elif response_time_ms > 2000:
                response.failure(
                    f"Slow response | {response_time_ms} ms"
                )
            else:
                response.success()


# ✅ Global request listener (Locust 2.x compatible)
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
