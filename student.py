import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Student Records Pro", page_icon="🎓", layout="wide"
)

# Custom CSS Styling for High-Visibility Text and Clean Cards
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f9;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.08);
        border-top: 5px solid #2b580c;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-title {
        font-size: 15px;
        color: #555555;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 28px;
        color: #111111;
        font-weight: bold;
    }
    .metric-delta {
        font-size: 13px;
        color: #0066cc;
        margin-top: 5px;
    }
    div.stButton > button {
        border-radius: 8px;
        font-weight: bold;
    }
    .search-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #ff4b4b;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("🎓 Student Records Management System")
st.markdown(
    "**Veda Technology** — Python Programming Track (Level 1 | Task 9: Advanced"
    " Features)"
)
st.markdown("---")

# Initialize Session State
if "student_names" not in st.session_state:
  st.session_state.student_names = [
      "Alice",
      "Bob",
      "Charlie",
      "Diana",
      "Ethan",
  ]
  st.session_state.student_marks = [85, 92, 78, 95, 88]


# Helper function to assign grades
def get_grade(mark):
  if mark >= 90:
    return "A (Excellent)"
  elif mark >= 80:
    return "B (Very Good)"
  elif mark >= 70:
    return "C (Good)"
  elif mark >= 60:
    return "D (Pass)"
  else:
    return "F (Fail)"


# --- SIDEBAR: MANAGEMENT TOOLS ---
st.sidebar.header("⚙️ Record Management")

# Add Student
st.sidebar.subheader("➕ Add New Student")
new_name = st.sidebar.text_input("Student Name")
new_mark = st.sidebar.slider("Marks (0-100)", 0, 100, 75)

if st.sidebar.button("Add Record", type="primary"):
  if new_name.strip() != "":
    st.session_state.student_names.append(new_name.strip())
    st.session_state.student_marks.append(new_mark)
    st.sidebar.success(f"Added {new_name} successfully!")
    st.rerun()
  else:
    st.sidebar.error("Please enter a valid name.")

st.sidebar.markdown("---")

# Update Student Marks
st.sidebar.subheader("✏️ Update Marks")
if st.session_state.student_names:
  update_student = st.sidebar.selectbox(
      "Select student to update", st.session_state.student_names, key="update_sel"
  )
  updated_mark = st.sidebar.slider(
      "New Marks", 0, 100, 75, key="update_slider"
  )
  if st.sidebar.button("Update Record"):
    idx = st.session_state.student_names.index(update_student)
    st.session_state.student_marks[idx] = updated_mark
    st.sidebar.success(f"Updated {update_student}'s marks to {updated_mark}!")
    st.rerun()

st.sidebar.markdown("---")

# Delete Student
st.sidebar.subheader("🗑️ Delete Student")
if st.session_state.student_names:
  student_to_delete = st.sidebar.selectbox(
      "Select student to remove", st.session_state.student_names, key="del_sel"
  )
  if st.sidebar.button("Delete Record"):
    idx = st.session_state.student_names.index(student_to_delete)
    st.session_state.student_names.pop(idx)
    st.session_state.student_marks.pop(idx)
    st.sidebar.success(f"Removed {student_to_delete}!")
    st.rerun()

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset to Default Data"):
  st.session_state.student_names = ["Alice", "Bob", "Charlie", "Diana", "Ethan"]
  st.session_state.student_marks = [85, 92, 78, 95, 88]
  st.sidebar.success("Reset data to defaults!")
  st.rerun()

# --- MAIN INTERFACE TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 View Directory",
    "📊 Statistics & Analytics",
    "🔍 Student Finder",
    "🔄 Sort & Filter",
    "📥 Export Data",
])

names = st.session_state.student_names
marks = st.session_state.student_marks

# Tab 1: View Records
with tab1:
  st.subheader("📋 Complete Student Directory")
  if names:
    df = pd.DataFrame({
        "Name": names,
        "Marks": marks,
        "Grade": [get_grade(m) for m in marks],
    })
    st.dataframe(df, use_container_width=True, hide_index=True)
  else:
    st.info("No records available. Add some students using the sidebar!")

# Tab 2: Statistics & Analytics
with tab2:
  st.subheader("📊 Performance Insights & Analytics")
  if marks:
    highest_score = max(marks)
    lowest_score = min(marks)
    avg_score = sum(marks) / len(marks)

    highest_students = [names[i] for i, m in enumerate(marks) if m == highest_score]
    lowest_students = [names[i] for i, m in enumerate(marks) if m == lowest_score]

    col1, col2, col3 = st.columns(3)

    with col1:
      st.markdown(
          f"""
            <div class="metric-card" style="border-top-color: #28a745;">
                <div class="metric-title">🏆 Highest Score</div>
                <div class="metric-value">{highest_score}</div>
                <div class="metric-delta">Student: {', '.join(highest_students)}</div>
            </div>
            """,
          unsafe_allow_html=True,
      )

    with col2:
      st.markdown(
          f"""
            <div class="metric-card" style="border-top-color: #dc3545;">
                <div class="metric-title">📉 Lowest Score</div>
                <div class="metric-value">{lowest_score}</div>
                <div class="metric-delta">Student: {', '.join(lowest_students)}</div>
            </div>
            """,
          unsafe_allow_html=True,
      )

    with col3:
      st.markdown(
          f"""
            <div class="metric-card" style="border-top-color: #007bff;">
                <div class="metric-title">📈 Class Average</div>
                <div class="metric-value">{avg_score:.2f}</div>
                <div class="metric-delta">Total Students: {len(marks)}</div>
            </div>
            """,
          unsafe_allow_html=True,
      )

    st.markdown("---")
    st.subheader("📋 Grade Breakdown Summary")
    grades_list = [get_grade(m).split()[0] for m in marks]
    grade_counts = {
        "A (90+)": grades_list.count("A"),
        "B (80-89)": grades_list.count("B"),
        "C (70-79)": grades_list.count("C"),
        "D (60-69)": grades_list.count("D"),
        "F (<60)": grades_list.count("F"),
    }
    st.bar_chart(grade_counts)

    st.markdown("---")
    st.subheader("Visual Student Marks Distribution")
    chart_data = pd.DataFrame({"Marks": marks}, index=names)
    st.bar_chart(chart_data)
  else:
    st.info("Add records to view analytics.")

# Tab 3: Search Student
with tab3:
  st.subheader("🔍 Quick Student Finder")
  search_query = st.text_input(
      "Type a student name to look up:", placeholder="e.g. Alice"
  )

  if search_query:
    found = False
    for i, name in enumerate(names):
      if name.lower() == search_query.strip().lower():
        st.markdown(
            f"""
                <div class="search-card">
                    <h3 style="color: #1f1f1f; margin-bottom: 5px;">✅ Record Found</h3>
                    <p style="font-size: 18px; color: #333333; margin: 0;"><b>Name:</b> {name}</p>
                    <p style="font-size: 18px; color: #333333; margin: 0;"><b>Marks:</b> {marks[i]}</p>
                    <p style="font-size: 18px; color: #333333; margin: 0;"><b>Grade:</b> {get_grade(marks[i])}</p>
                </div>
                """,
            unsafe_allow_html=True,
        )
        found = True
        break
    if not found:
      st.warning(f"❌ No student named '{search_query}' found in the directory.")

# Tab 4: Sort & Filter
with tab4:
  st.subheader("🔄 Reorder & Filtering Options")
  sort_order = st.radio(
      "Choose sorting order:",
      ["Descending (Highest to Lowest)", "Ascending (Lowest to Highest)"],
  )

  combined = list(zip(names, marks))
  if "Descending" in sort_order:
    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)
  else:
    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=False)

  s_names = [item[0] for item in sorted_combined]
  s_marks = [item[1] for item in sorted_combined]

  sorted_df = pd.DataFrame({
      "Name": s_names,
      "Marks": s_marks,
      "Grade": [get_grade(m) for m in s_marks],
  })
  st.dataframe(sorted_df, use_container_width=True, hide_index=True)

# Tab 5: Export Data
with tab5:
  st.subheader("📥 Export Records")
  if names:
    export_df = pd.DataFrame(
        {"Name": names, "Marks": marks, "Grade": [get_grade(m) for m in marks]}
    )
    csv = export_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Records as CSV File",
        data=csv,
        file_name="student_records.csv",
        mime="text/csv",
        type="primary",
    )
  else:
    st.info("No data available to export.")