let subjectCount = 1;

function addRow() {

    subjectCount++;

    const tableBody = document.getElementById("tableBody");

    const row = document.createElement("tr");

    row.innerHTML = `
        <td>
            <select name="subject${subjectCount}" required>

                <option value="">Select Subject</option>

                <option>Math</option>
                <option>Physics</option>
                <option>Chemistry</option>
                <option>English</option>
                <option>Biology</option>
                <option>Programming</option>
                <option>History</option>
                <option>Economics</option>
                <option>AI</option>
                <option>DBMS</option>

            </select>
        </td>

        <td>
            <input
                type="number"
                name="hours${subjectCount}"
                min="1"
                max="6"
                required>
        </td>

        <td>
            <button
                type="button"
                class="delete-btn"
                onclick="removeRow(this)">
                ❌
            </button>
        </td>
    `;

    tableBody.appendChild(row);
}

function removeRow(button) {

    const tableBody = document.getElementById("tableBody");

    // Don't remove the last remaining row
    if (tableBody.rows.length === 1) {
        alert("At least one subject is required.");
        return;
    }

    button.closest("tr").remove();
}