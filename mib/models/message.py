class Message():
    """Representation of Message model."""

    def __init__(self,
                 id=None,
                 sender_id=None,
                 recipient_id=None,
                 text=None,
                 delivery_date=None,
                 is_draft=None,
                 is_delivered=None,
                 is_read=None
        ):
        #Data
        self.id = id
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.text = text
        self.delivery_date = delivery_date
        self.sender = {'first_name': None, 'last_name': None}
        self.recipient = {'first_name': None, 'last_name': None}
        # Booleans
        self.is_draft = is_draft
        self.is_delivered = is_delivered
        self.is_read = is_read
 