#include <MQTT.h>
#include <Grove-Ultrasonic-Ranger.h>

// Ultrasonic object constructor
Ultrasonic ultrasonic(D4);

// Callback (Unused as the Rpi won't be sending info the the Argon)
MQTT client("test.mosquitto.org", 1883, callback);

void callback(char *topic, byte *payload, unsigned int length)
{
}

void setup()
{
    client.connect("argon_dev");

    // Begin serial communications
    Serial.begin(9600);
}

void loop()
{
    // Assign variable for the distance measurement
    long RangeInCentimeters;

    // Calculate the current distance value
    RangeInCentimeters = ultrasonic.MeasureInCentimeters();

    // Out put the value over serial
    Serial.print(RangeInCentimeters);

    // Use 'particle serial monitor --follow' in the CLI to see serial output
    Serial.println(" cm");

    // // Set a small delay, so the sensor has some time to recalculate the distance
    // delay(1000);

    if (client.isConnected())
    {
        client.publish("argonLog", String(RangeInCentimeters));
        delay(300);
    }

    client.loop();
}
