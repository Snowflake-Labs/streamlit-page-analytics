# Streamlit Page Analytics

A Python library for building page analytics in Streamlit applications through logging.

The solution instruments all `st.<widget>` with a wrapper function which emits logs,
these logs can then be processed to derive analytics information.

This solution is inspired from [jrieke/streamlit-analytics](https://github.com/jrieke/streamlit-analytics) idea.

Events are emitted as **JSON objects** (one object per log record) via Python’s `logging` API, using the configured logger and log level (default `INFO`).

### Log format

Each line is a single JSON object produced from a `UserEvent` (or equivalent) after enrichment:

| Field | Meaning |
|-------|---------|
| `session_id` | From `StreamlitPageAnalytics` (constructor or `set_session_id`) |
| `user_id` | From `StreamlitPageAnalytics` (constructor or `set_user_id`) |
| `page_name` | Present when page tracking is active and set |
| `action` | Event type (string); see table below |
| `widget` | Present when the event targets a widget (id, type, label, values, etc.); omitted when empty |
| `extra` | Additional payload (form field snapshots, notices, etc.); omitted when empty |

Empty or null values are typically **omitted** from the JSON (`clean_values`).

**`action` values** (see `UserEventAction` in code): `start_tracking`, `form_instrumentation_notice`, `click`, `change`, `submit`, `other`.

## Installation
Use the releases to download assets:

### Local
To run it locally, Download the wheel(`.whl`) file and install or
install from git:

```bash
pip install \
git+https://github.com/Snowflake-Labs/streamlit-page-analytics@latest
```
### Streamlit in Snowflake (SiS)
Download the `streamlit_page_analytics-<version>.zip` file and copy it to a
Snowflake Internal Stage for use in SiS and run the following command:

```snowflake
ALTER STREAMLIT <your-streamlit-name> SET 
  IMPORTS = ('@<your-internal-stage>/<path/to/your/zip/file>');
```

## Usage

```python
import streamlit as st
from streamlit_page_analytics import StreamlitPageAnalytics

with StreamlitPageAnalytics.track(
    name="my-app", session_id=f"{session_id}", user_id=f"{user_id}"
):

    st.title("My Awesome App")
    st.button('my awesome button')
```

or

```python
import streamlit as st
from streamlit_page_analytics import StreamlitPageAnalytics

page_analytics = StreamlitPageAnalytics(
        name="my-app", session_id=f"{session_id}", user_id=f"{user_id}"
)

page_analytics.start_tracking()

st.title("My Awesome App")
st.button('my awesome button')

page_analytics.stop_tracking()
```

### Page Tracking

Track page visits in multi-page Streamlit applications by passing a `page_name` to `start_tracking()`. A `start_tracking` event is logged only when the user navigates to a different page, avoiding duplicate logs on page reruns.

```python
import streamlit as st
from streamlit_page_analytics import StreamlitPageAnalytics

page_analytics = StreamlitPageAnalytics(
    name="my-app", session_id=f"{session_id}", user_id=f"{user_id}"
)

# Pass the current page name - logs only when page changes
page_analytics.start_tracking(page_name="Home")

st.title("Home Page")
st.button("Click me")

page_analytics.stop_tracking()
```

When the user navigates between pages:
- `start_tracking(page_name="Home")` - Logs (first visit)
- `start_tracking(page_name="Home")` - No log (same page, e.g., rerun)
- `start_tracking(page_name="Settings")` - Logs (different page)
- `start_tracking(page_name="Home")` - Logs (navigated back)

If `page_name` is not provided or is empty, no page tracking event is logged.

### Forms (`st.form`)

Streamlit does not allow `on_change` / `on_click` on widgets inside a form except on `st.form_submit_button`. This library therefore does **not** attach per-widget analytics callbacks to inputs inside `st.form()`. Instead:

- **One-time notice (`form_instrumentation_notice`)** — The first time a tracked widget is created inside a form in a session, the library logs a single event through the same **`log_event`** path as every other analytics event, so **`session_id`**, **`user_id`**, and optional **`page_name`** match the rest of the stream. The human-readable explanation is in **`extra.message`**. There is usually **no `widget`** on this object after serialization (same as other events with no element).
- **Submit (`submit`)** — When the user presses **`st.form_submit_button`**, a **`submit`** event is logged. The **submit button** appears under **`widget`**. Registered field values at submit time are in top-level **`extra`**: **`extra.form_id`** and **`extra.form_fields`** (each entry: id, type, label, value). Masking options apply to text inputs and text areas in that snapshot the same way as elsewhere.
- If you pass your own `on_change` or `on_click` on a widget **inside** a form, Streamlit may reject it or it conflicts with form rules; this package does **not** forward those developer callbacks for form widgets. Use callbacks on `st.form_submit_button` if you need custom logic on submit.

### Masking Text Input Values

For privacy-sensitive applications, you can mask the values of `text_input` and `text_area` widgets in the logs by setting `mask_text_input_values=True`. When enabled, the actual input values will be replaced with `"[REDACTED]"` in the log output.

```python
import streamlit as st
from streamlit_page_analytics import StreamlitPageAnalytics

with StreamlitPageAnalytics.track(
    name="my-app",
    session_id=f"{session_id}",
    user_id=f"{user_id}",
    mask_text_input_values=True,  # Enable masking for text inputs
):
    st.text_input("Password")  # Value will be logged as "[REDACTED]"
    st.text_area("Notes")      # Value will be logged as "[REDACTED]"
    st.selectbox("Option", ["A", "B"])  # Not affected, logs actual value
```

## Current Status

The following Streamlit widgets are currently supported:
- `st.button` - Click events
- `st.form_submit_button` - Submit events; combined snapshot of tracked form fields in `extra.form_fields` when used inside `st.form()`
- `st.checkbox` - Change events
- `st.radio` - Change events
- `st.selectbox` - Change events
- `st.multiselect` - Change events
- `st.slider` - Change events
- `st.select_slider` - Change events
- `st.text_input` - Change events
- `st.number_input` - Change events
- `st.text_area` - Change events
- `st.date_input` - Change events
- `st.time_input` - Change events
- `st.file_uploader` - Change events
- `st.color_picker` - Change events


## Analytics Tables
Use the sample [analytics script](dashboard/snowflake_views_dynamic_tables.sql) to setup analytics on top of the
logs can be quickly built using dynamic tables.

## Developer documentation

- **[DEVELOPMENT.md](DEVELOPMENT.md)** — Workflow, tasks, and how integration tests assert on JSON logs.
- **[LINTING.md](LINTING.md)** — Linter configuration and commands.

## Disclaimer
License: Apache 2.0

This is not an official Snowflake product or feature.
