# Streamlit Page Analytics

A Python library for building page analytics in Streamlit applications through logging.

The solution instruments all `st.<widget>` with a wrapper function which emits logs,
these logs can then be processed to derive analytics information.

This solution is inspired from [jrieke/streamlit-analytics](https://github.com/jrieke/streamlit-analytics) idea.

## Installation

```bash
pip install streamlit_page_analytics
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

## Disclaimer
License: Apache 2.0

This is not an official Snowflake product or feature.
