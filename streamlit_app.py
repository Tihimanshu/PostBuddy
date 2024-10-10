import streamlit as st
import openai
import datetime
import json

# Custom GPT Link (replace with your actual link)
CUSTOM_GPT_LINK = "https://chatgpt.com/g/g-TsgWYXEAy-social-post-maestro"

# Billing plans
def billing_plans():
    st.sidebar.title("Billing Plan")
    plan = st.sidebar.radio("Select a Plan", ["Free", "$10/month", "$20/month", "$50/month"])
    if plan == "Free":
        st.sidebar.write("2 posts per month")
        return 2
    elif plan == "$10/month":
        st.sidebar.write("15 posts per month")
        return 15
    elif plan == "$20/month":
        st.sidebar.write("40 posts per month")
        return 40
    elif plan == "$50/month":
        st.sidebar.write("100 posts per month")
        return 100

# History manager
def save_to_history(history, text):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if len(history) >= 10:
        history.pop(0)  # Keep only last 10 posts
    history.append({"timestamp": timestamp, "text": text})
    return history

def main():
    st.title("LinkedIn Social Post Maestro")
    st.write("Use the custom GPT tool to generate LinkedIn posts for various topics")

    # Sidebar for history and billing management
    with open('history.json', 'r') as f:
        history = json.load(f)

    st.sidebar.title("Post History")
    for item in reversed(history):
        st.sidebar.write(f"{item['timestamp']}: {item['text'][:20]}...")

    post_limit = billing_plans()

    # User Input Section
    topic = st.selectbox("Choose a topic", ["Marketing", "Product", "Sales", "Customer Success", "Founder", "Team Building", "Corporate", "Mental Health", "Investment", "Custom"])
    if topic == "Custom":
        topic = st.text_input("Enter a custom topic:")
    tone = st.selectbox("Choose a tone", ["Professional", "Casual", "Motivational", "Humorous"])
    format = st.selectbox("Choose a format", ["Short LinkedIn Post", "Detailed LinkedIn Post", "Question & Engagement Post", "Storytelling"])

    # Generate Button
    if st.button("Generate Post"):
        # Generate response using GPT
        openai.api_key = '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'  # Replace with your OpenAI API key
        prompt = f"Write a {format} post about {topic} with a {tone} tone"
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=150
        )
        generated_text = response.choices[0].text.strip()

        st.subheader("Generated Post")
        st.write(generated_text)

        # Copy button
        st.button("Copy to Clipboard", on_click=lambda: st.experimental_set_query_params(post=generated_text))

        # Save to history
        with open('history.json', 'w') as f:
            json.dump(save_to_history(history, generated_text), f)

    st.sidebar.title("Manage History")
    if st.sidebar.button("Clear History"):
        with open('history.json', 'w') as f:
            json.dump([], f)
        st.sidebar.success("History cleared.")

if __name__ == '__main__':
    try:
        with open('history.json', 'x') as f:
            json.dump([], f)
    except FileExistsError:
        pass
    main()
