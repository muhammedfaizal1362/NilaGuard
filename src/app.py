from evaluation import calculate_metrics
import streamlit as st
from analyzer import analyze_message
from url_analyzer import analyze_url

st.set_page_config(
    page_title="NilaGuard",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ NilaGuard")
st.subheader("Privacy-First Scam Indicator Analyzer")

st.caption(
    "Analyze suspicious messages and URLs using "
    "static, explainable indicators."
)

option = st.selectbox(
    "Choose analysis type",
    ["Message Analysis", "URL Analysis"]
)

if option == "Message Analysis":

    message = st.text_area(
        "Enter a message to analyze"
    )

    if st.button("Analyze Message"):

        if not message.strip():
            st.warning("Please enter a message.")

        else:
            result = analyze_message(message)

            st.metric(
                "Indicator Score",
                f"{result['score']}/100"
            )

            st.write("Result:", result["level"])

            st.write("Explanation:")
            st.write(result["message"])

            if result["findings"]:
                st.write("Detected indicators:")

                for finding in result["findings"]:
                    st.write(
                        f"- {finding['category']}: "
                        f"{finding['matched_indicator']}"
                    )
            else:
                st.info("No predefined indicators detected.")

elif option == "URL Analysis":

    url = st.text_input("Enter a URL")

    if st.button("Analyze URL"):

        if not url.strip():
            st.warning("Please enter a URL.")

        else:
            result = analyze_url(url)

            st.write("Valid format:", result["valid"])

            if result.get("hostname"):
                st.write("Hostname:", result["hostname"])

            st.write("Findings:")

            if result["findings"]:
                for finding in result["findings"]:
                    st.warning(finding)
            else:
                st.success("No predefined structural indicators detected.")

            st.caption(result["message"])

st.divider()

st.subheader("Dataset Evaluation")
st.subheader("Confusion Matrix")

matrix = [
    [metrics["tp"], metrics["fn"]],
    [metrics["fp"], metrics["tn"]],
]

st.write("Rows = Actual | Columns = Predicted")

st.dataframe(
    {
        "Predicted Indicator": [metrics["tp"], metrics["fp"]],
        "Predicted Normal": [metrics["fn"], metrics["tn"]],
    },
    use_container_width=True,
)
metrics = calculate_metrics()

st.write("Test samples:", metrics["total"])
st.write("True Positives:", metrics["tp"])
st.write("True Negatives:", metrics["tn"])
st.write("False Positives:", metrics["fp"])
st.write("False Negatives:", metrics["fn"])

st.metric("Accuracy", f'{metrics["accuracy"]}%')
st.metric("Precision", f'{metrics["precision"]:.2f}')
st.metric("Recall", f'{metrics["recall"]:.2f}')
st.metric("F1 Score", f'{metrics["f1"]:.2f}')

st.caption(
    "Results are from a small synthetic dataset "
    "and do not represent real-world performance."
)
