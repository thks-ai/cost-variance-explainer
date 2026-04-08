# app/database/models.py

class Variance:
    def __init__(self, id, period, item_code, item_name, department,
                 actual_cost, standard_cost, quantity,
                 variance_amount, variance_type, created_at):
        self.id = id
        self.period = period
        self.item_code = item_code
        self.item_name = item_name
        self.department = department
        self.actual_cost = actual_cost
        self.standard_cost = standard_cost
        self.quantity = quantity
        self.variance_amount = variance_amount
        self.variance_type = variance_type
        self.created_at = created_at


class ReasonLog:
    def __init__(self, id, variance_id, ai_generated, user_final, created_at):
        self.id = id
        self.variance_id = variance_id
        self.ai_generated = ai_generated
        self.user_final = user_final
        self.created_at = created_at


class EmbeddingStore:
    def __init__(self, id, reason_log_id, text, vector_path,
                 item_code, department, variance_type, variance_amount, created_at):
        self.id = id
        self.reason_log_id = reason_log_id
        self.text = text
        self.vector_path = vector_path
        self.item_code = item_code
        self.department = department
        self.variance_type = variance_type
        self.variance_amount = variance_amount
        self.created_at = created_at
