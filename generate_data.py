async def generateData(client):
    
    global print_status, exercise, sample

    try:
        # Initialize process
        setInitialDateTimeStamp()
        updateExerciseNumber()

        print_status = "ready"
        print(f"   Ready to start exercise {exercise}!")

        # Start notifications
        await client.start_notification(HANDLE_READ_DATA)
        
        while True:
            if exercise == -1:
                break

            await asyncio.sleep(0)

            # Keyboard management
            if keyboard.is_pressed("x"):    # Exit
                if print_status == "recording":
                    print(f"      ...End data collection exercise {exercise} / sample {sample}")
                    client.data_file.close()
                    print('File closed')

                print("Data collection terminated")
                break

            elif keyboard.is_pressed("s"):  # Start collecting data
                if print_status != "recording":
                    sample += 1
                    print(f"      Start data collection exercise {exercise} / sample {sample}...")
                    print_status = "recording"
            
                    client.data_file = openFile()

            elif keyboard.is_pressed("e"):  # Stop data collection
                if print_status == "recording":
                    print(f"      ...End data collection exercise {exercise} / sample {sample}")
                    print_status = "stopped"
                    client.data_file.close()
                    print('File closed')
            
            elif keyboard.is_pressed("n"):  # Prepare system for new exercise
                if print_status != "ready":
                    if print_status == "recording":
                        print(f"      ...End data collection exercise {exercise} / sample {sample}")
                        client.data_file.close()
                        print('File closed')

                    updateExerciseNumber()
                    print(f"   Ready to start exercise {exercise}")
                    print_status = "ready"
                
                    sample = 0

        # Stop notifications
        await client.stop_notification(HANDLE_READ_DATA)

    except Exception as e:
        print(f"AIR Error: {e}")

    finally:
        try:
            client.data_file.close()
            print('File closed')
        except:
            pass
        finally:
            keyboard.send('esc')

    print('Data capture complete')
    return


