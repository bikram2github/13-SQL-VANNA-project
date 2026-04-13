import asyncio
from vanna.capabilities.agent_memory import ToolMemory
from vanna.core.tool import ToolContext
from vanna.core.user import User
from vanna_setup import setup_vanna


def get_training_data():
    return [
        ("How many patients are there?", "SELECT COUNT(*) FROM patients;"),
        ("How many doctors are available?", "SELECT COUNT(*) FROM doctors;"),
        ("List top 5 patients by total spending", """
            SELECT patient_id, SUM(total_amount) AS total_spending
            FROM invoices
            GROUP BY patient_id
            ORDER BY total_spending DESC
            LIMIT 5;
        """),
        ("Total revenue generated", "SELECT SUM(total_amount) FROM invoices;"),
        ("Pending invoices count", "SELECT COUNT(*) FROM invoices WHERE status = 'Pending';"),
        ("Show all doctors and their specialization", "SELECT name, specialization FROM doctors;"),
        ("Appointments count by status", """
            SELECT status, COUNT(*) 
            FROM appointments 
            GROUP BY status;
        """),
        ("Average treatment cost", "SELECT AVG(cost) FROM treatments;"),
        ("Top 3 doctors with most appointments", """
            SELECT doctor_id, COUNT(*) as total
            FROM appointments
            GROUP BY doctor_id
            ORDER BY total DESC
            LIMIT 3;
        """),
        ("Total unpaid amount", """
            SELECT SUM(total_amount - paid_amount) 
            FROM invoices;
        """),
        ("Patients registered in last 30 days", """
            SELECT COUNT(*) 
            FROM patients
            WHERE registered_date >= DATE('now', '-30 days');
        """),
        ("Most common treatment", """
            SELECT treatment_name, COUNT(*) as count
            FROM treatments
            GROUP BY treatment_name
            ORDER BY count DESC
            LIMIT 1;
        """),
        ("Total appointments per doctor", """
            SELECT doctor_id, COUNT(*) 
            FROM appointments 
            GROUP BY doctor_id;
        """),
        ("Show invoices with overdue status", "SELECT * FROM invoices WHERE status = 'Overdue';"),
        ("Total number of treatments", "SELECT COUNT(*) FROM treatments;")
    ]


async def seed_memory():
    agent, _ = setup_vanna()

    user = User(
        id="admin",
        email="admin@example.com",
        group_memberships=["admin"]
    )

    training_data = get_training_data()

    for i, (question, sql) in enumerate(training_data):
        print(f"Training {i+1}/{len(training_data)}: {question}")

        context = ToolContext(
            user=user,
            conversation_id=f"seed-{i}",
            request_id=f"req-{i}",
            agent_memory=agent.agent_memory
        )

        await agent.agent_memory.save_tool_usage(
            question=question,
            tool_name="RunSqlTool",
            args={"query": sql.strip()},
            context=context,
            success=True
        )

    print("\n✅ ALL DATA TRAINED SUCCESSFULLY!")


if __name__ == "__main__":
    asyncio.run(seed_memory())