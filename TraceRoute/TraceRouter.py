class TraceRouter:

    def __init__(self, hop_user_inputs_model):
        self.hop_user_inputs_model = hop_user_inputs_model


    def start_hop(self):
        for item in range(1,self.hop_user_inputs_model.hop_tries + 1):
            pass

    def start_ttl(self):
        pass