from dataclasses import dataclass
import time

@dataclass
class WaterLevel:
    tank_id: str
    water_level_precentage: int

@dataclass
class WaterRefillingProgres:
    tank_id: str
    water_level_precentage: int

@dataclass
class WaterDroppingProgres:
    tank_id: str
    water_level_precentage: int


class WaterLevelCheck:
    def __init__(self, tank_id):
        self.tank_id=tank_id
        self.water_level=100
        
    def update_water_level(self,water_level):
        self.water_level_precentage = water_level
        if self.water_level_precentage < 15:
            return WaterLevel(self.tank_id,self.water_level_precentage)
        return None

    def get_water_info(self):
        return WaterLevel(self.tank_id,self.water_level_precentage)

    def add_water(self,ammount):
        if self.water_level_precentage + ammount >100:
            self.water_level_precentage=100
        else:
            self.water_level_precentage += ammount            
        return WaterRefillingProgres(self.tank_id,self.water_level_precentage)
    
    def remove_water(self,ammount):
        if self.water_level_precentage - ammount <0:
            self.water_level_precentage=00
        else:
            self.water_level_precentage -= ammount            
        return WaterDroppingProgres(self.tank_id,self.water_level_precentage)

class SmsService:
    def send_sms(self, event):
        print(f"Sms service for {event.tank_id}")

class PumpController:
    def __init__(self,bus,tank):
        self.bus=bus
        self.tank=tank

    def start_puump(self,event):
        print(f"Water level for {event.tank_id} is  {event.water_level_precentage} < 15%. Pump controll on.")
        for i in range(1,5):
            time.sleep(1)
            print(f"Water is pooring..")
            refill_event = self.tank.add_water(10)
            self.bus.publish(refill_event)

    def water_level_info(self,event):
        print(f"Info: tank {event.tank_id} water level: {event.water_level_precentage}")

    def drop_bucket_of_water(self,event):
        print("drop_bucket_of_water: bucket of water is going to drop")
        print(f"Level before: {event.water_level_precentage}")
        time.sleep(1)
        drop_event = self.tank.remove_water(5)
        self.bus.publish(drop_event)




class EventBus:
    def __init__(self):
        self._handler = {}

    def add_subscribtion_event(self,event_type,handler):
        if event_type not in self._handler:
            self._handler[event_type]=[]

        self._handler[event_type].append(handler)
        print(2)

    def publish(self,event):
        event_type = type(event)
        one_type_handler = self._handler.get(event_type)    #it takes all expected subscribers (added before) -mosty their metod to run

        if one_type_handler is None:return

        for h in one_type_handler:
            h(event)    #h -pointer to funciton, event -param for that funciton

tank = WaterLevelCheck("T12")
bus = EventBus()
sms = SmsService()
pump = PumpController(bus,tank)
bus.add_subscribtion_event(WaterLevel,sms.send_sms)
bus.add_subscribtion_event(WaterLevel,pump.start_puump)
bus.add_subscribtion_event(WaterRefillingProgres,pump.water_level_info)
bus.add_subscribtion_event(WaterDroppingProgres,pump.water_level_info)


e = tank.update_water_level(10)

bus.publish(e)

e=tank.remove_water(10)

bus.publish(e)