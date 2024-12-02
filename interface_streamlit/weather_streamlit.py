import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

st.title("PCA on Weather Dataset")

st.subheader("Original Dataset")
st.dataframe(df.head())

st.subheader("Explained Variance by Components")
fig, ax = plt.subplots()
ax.plot(np.cumsum(explained_variance), marker='o', linestyle='--')
ax.set_title('Cumulative Explained Variance')
ax.set_xlabel('Number of Components')
ax.set_ylabel('Explained Variance')
st.pyplot(fig)

st.subheader("PCA Reduced Data")
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='PCA1', y='PCA2', hue='Summary', ax=ax)
ax.set_title('PCA Visualization (2 Components)')
st.pyplot(fig)
