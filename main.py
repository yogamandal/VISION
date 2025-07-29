# # import os
# # import glob

# # # Delete previously captured images
# # def clear_old_images(folder="captured_images"):
# #     if not os.path.exists(folder):
# #         os.makedirs(folder)
# #         return
# #     for file_path in glob.glob(os.path.join(folder, "*.jpg")):
# #         try:
# #             os.remove(file_path)
# #         except Exception as e:
# #             print(f"⚠️ Could not delete {file_path}: {e}")

# # # Clear old images at the beginning
# # clear_old_images()

# # import time
# # from scene_description.webcam_capture import capture_image
# # from scene_description.describe_scene import describe_image
# # from scene_description.speak import speak

# # DELAY_SECONDS = 10

# # def main_loop():
# #     print("🔁 Starting scene description loop. Press Ctrl+C to stop.")
# #     while True:
# #         try:
# #             print("📸 Capturing image...")
# #             image_path = capture_image()
# #             print("✅ Image captured!")

# #             print("🧠 Describing image...")
# #             description = describe_image(image_path)
# #             print(f"🖼️ Scene Description: {description}")

# #             print("🗣️ Speaking...")
# #             speak(description)

# #             print("⏳ Waiting for next capture...")
# #             time.sleep(DELAY_SECONDS)

# #         except KeyboardInterrupt:
# #             print("\n🛑 Stopped by user.")
# #             break
# #         except Exception as e:
# #             print(f"❌ Error: {e}")
# #             time.sleep(5)

# # # def main_loop():
# # #     print("Starting scene description loop. Press Ctrl+C to stop.")
# # #     while True:
# # #         try:
# # #             image_path = capture_image()
# # #             description = describe_image(image_path)
# # #             print(f"🖼️ Scene: {description}")
# # #             speak(description)
# # #             time.sleep(DELAY_SECONDS)
# # #         except KeyboardInterrupt:
# # #             print("\n🛑 Stopped by user.")
# # #             break
# # #         except Exception as e:
# # #             print(f"❌ Error: {e}")
# # #             time.sleep(5)

# # if __name__ == "__main__":
# #     main_loop()


# # adding sppech regonition 
# import os
# import glob
# import time

# from scene_description.webcam_capture import capture_image
# from scene_description.describe_scene import describe_image
# from scene_description.speak import speak
# # from scene_description.listen import listen_for_trigger
# from scene_description.listen_vosk import listen_for_command


# # Delete previously captured images
# def clear_old_images(folder="captured_images"):
#     if not os.path.exists(folder):
#         os.makedirs(folder)
#         return
#     for file_path in glob.glob(os.path.join(folder, "*.jpg")):
#         try:
#             os.remove(file_path)
#         except Exception as e:
#             print(f"⚠️ Could not delete {file_path}: {e}")

# def main():
#     clear_old_images()
#     print("🎬 Voice-triggered scene assistant started. Say 'describe' to begin.")

#     while True:
#         try:
#             print("🎤 Listening for trigger...")
#             if listen_for_trigger():
#                 print("📸 Capturing image...")
#                 image_path = capture_image()
#                 print(f"✅ Image captured: {image_path}")

#                 print("🧠 Describing image...")
#                 description = describe_image(image_path)
#                 print(f"🖼️ Scene Description: {description}")

#                 print("🗣️ Speaking description...")
#                 speak(description)
#             else:
#                 print("🔇 Trigger not detected. Listening again...\n")

#         except KeyboardInterrupt:
#             print("\n🛑 Assistant stopped by user.")
#             break
#         except Exception as e:
#             print(f"❌ Error: {e}")
#             time.sleep(3)

# if __name__ == "__main__":
#     main()

# # main.py with Vosk integration + command matching
import os
import time
from scene_description.webcam_capture import capture_image
from scene_description.describe_scene import describe_image
from scene_description.speak import speak
from scene_description.listen_vosk import listen_for_command

def clear_old_images(folder="captured_images"):
    if not os.path.exists(folder):
        os.makedirs(folder)
        return
    for file_name in os.listdir(folder):
        if file_name.endswith(".jpg"):
            try:
                os.remove(os.path.join(folder, file_name))
            except Exception as e:
                print(f"⚠️ Could not delete {file_name}: {e}")

def command_matches(text):
    # Simple, extendable way to match multiple possible commands
    TRIGGERS = [
        "describe", "what do you see", "capture", "environment",
        "tell me what you see", "can you see", "scene", "picture", "show me"
    ]
    text = text.lower()
    return any(trigger in text for trigger in TRIGGERS)

def main():
    clear_old_images()
    print("🎬 Voice-triggered scene assistant started (offline mode with Vosk).")
    print("🎤 Say something like 'describe', 'what do you see', or 'capture again'...\n")

    while True:
        try:
            print("🎧 Listening for command...")
            command = listen_for_command()

            if command_matches(command):
                print("📸 Capturing image...")
                image_path = capture_image()
                print(f"✅ Image captured: {image_path}")

                print("🧠 Describing image...")
                description = describe_image(image_path)
                print(f"🖼️ Scene Description: {description}")

                print("🗣️ Speaking description...")
                speak(description)
            else:
                print("🔇 No valid command detected. Heard:", command)

        except KeyboardInterrupt:
            print("\n🛑 Assistant stopped by user.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(3)

if __name__ == "__main__":
    main()
