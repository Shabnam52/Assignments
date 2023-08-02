const fetchButton = document.getElementById('fetchButton');
const employeeIdInput = document.getElementById('employeeId');
const resumeContent = document.getElementById('resumeContent');

fetchButton.addEventListener('click', () => {
    const employeeId = employeeIdInput.value;
    if (!employeeId) {
        alert('Please enter an Employee ID.');
        return;
    }

    fetch(`/api/employees/${employeeId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Employee not found.');
            }
            return response.json();
        })
        .then(data => displayResume(data))
        .catch(error => {
            console.error('Error fetching employee details:', error);
            resumeContent.innerHTML = `<p>Error: ${error.message}</p>`;
        });
});

function displayResume(employee) {
    if (employee.error) {
        resumeContent.innerHTML = `<p>${employee.error}</p>`;
    } else {
        resumeContent.innerHTML = `
            <h2>Resume for ${employee.name}</h2>
            <p><strong>Designation:</strong> ${employee.designation}</p>
            <p><strong>Professional Summary:</strong></p>
            <p>${employee.summary}</p>
            <p><strong>Technical Skills:</strong></p>
            <p>${employee.technical_skills}</p>
        `;

        // Generate and download resume as PDF
        generateAndDownloadPDF(employee);
    }
}

function generateAndDownloadPDF(employee) {
    const docDefinition = {
        content: [
            { text: `Resume for ${employee.name}`, style: 'header' },
            { text: `Designation: ${employee.designation}`, style: 'subheader' },
            { text: 'Professional Summary:', style: 'subheader' },
            { text: employee.summary, style: 'content' },
            { text: 'Technical Skills:', style: 'subheader' },
            { text: employee.technical_skills, style: 'content' }
        ],
        styles: {
            header: { fontSize: 18, bold: true, margin: [0, 10, 0, 5] },
            subheader: { fontSize: 14, bold: true, margin: [0, 5, 0, 3] },
            content: { fontSize: 12, margin: [0, 0, 0, 10] }
        }
    };

    // Generate the PDF
    const pdfDocGenerator = pdfMake.createPdf(docDefinition);

    // Download the PDF
    pdfDocGenerator.download(`Resume_${employee.name}.pdf`);
}
