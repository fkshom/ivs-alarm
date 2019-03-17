
from logging import basicConfig, getLogger, DEBUG
import ivs_alarm.ivs_alarm

basicConfig(level=DEBUG, format="%(asctime)s - %(levelname)-5s - %(filename)s(L%(lineno) 3d) - %(name)s - \n*** %(message)s")

def main():
    ivs_alarm.ivs_alarm.main()

if __name__ == "__main__":
    main()