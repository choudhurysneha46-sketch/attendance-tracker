async function loadSubjects() {
  const res = await fetch(`${API_URL}/api/subjects`);
  const subjects = await res.json();

  const list = document.getElementById("subjectList");
  list.innerHTML = "";

  if (subjects.length === 0) {
    list.innerHTML = "<p>No subjects yet. Add one above!</p>";
    return;
  }

  subjects.forEach(sub => {
    const isGood = sub.percentage >= 75;
    const card = document.createElement("div");
    card.className = "subject-card";
    card.innerHTML = `
      <div class="subject-card-top">
        <h3>${sub.name}</h3>
        <span class="percentage ${isGood ? "good" : "bad"}">${sub.percentage}%</span>
      </div>
      <div class="stats">Attended ${sub.attended_classes} / ${sub.total_classes} classes</div>
      <div class="subject-actions">
        <button class="present-btn" onclick="logClass(${sub.id}, true)">Present</button>
        <button class="absent-btn" onclick="logClass(${sub.id}, false)">Absent</button>
        <button class="delete-btn" onclick="deleteSubject(${sub.id})">Delete</button>
      </div>
    `;
    list.appendChild(card);
  });
}

async function addSubject() {
  const input = document.getElementById("subjectName");
  const name = input.value.trim();
  if (!name) return alert("Enter a subject name first");

  const res = await fetch(`${API_URL}/api/subjects`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name })
  });

  if (!res.ok) {
    const err = await res.json();
    return alert(err.error || "Something went wrong");
  }

  input.value = "";
  loadSubjects();
}

async function logClass(id, present) {
  await fetch(`${API_URL}/api/subjects/${id}/log`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ present })
  });
  loadSubjects();
}

async function deleteSubject(id) {
  if (!confirm("Delete this subject?")) return;
  await fetch(`${API_URL}/api/subjects/${id}`, { method: "DELETE" });
  loadSubjects();
}

// Load subjects when page opens
loadSubjects();
