# Streamlit Page Analytics

A Python library for building page analytics in Streamlit applications through logging.

The solution instruments all `st.<widget>` with a wrapper function which emits logs,
these logs can then be processed to derive analytics information.

This solution is inspired from [jrieke/streamlit-analytics](https://github.com/jrieke/streamlit-analytics) idea.

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

## Disclaimer
License: Apache 2.0

This is not an official Snowflake product or feature.
