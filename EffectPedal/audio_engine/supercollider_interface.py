from pythonosc.udp_client import SimpleUDPClient

class SuperColliderInterface:
    def __init__(self, ip="127.0.0.1", port=57120):
        self.client = SimpleUDPClient(ip, port)

    def start_effect(self, effect_name, **params):
        param_list = [params[key] for key in sorted(params.keys())]
        self.client.send_message(f"/{effect_name}/start", param_list)
        print(f"Started {effect_name} with params: {params}")

    def update_effect(self, effect_name, **params):
        param_list = [params[key] for key in sorted(params.keys())]
        self.client.send_message(f"/{effect_name}/update", param_list)
        print(f"Updated {effect_name} with params: {params}")

    def stop_effect(self, effect_name):
        self.client.send_message(f"/{effect_name}/stop", [])
        print(f"Stopped {effect_name}")

if __name__ == "__main__":
    sc_interface = SuperColliderInterface()
    
    # Example Usage
    sc_interface.start_effect("granular", rate=1.2, grain_size=0.15, density=12, pan=-0.5, amp=0.7)
    sc_interface.update_effect("granular", rate=0.8)
    sc_interface.stop_effect("granular")
