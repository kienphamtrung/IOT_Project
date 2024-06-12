package com.ryanhoangt.demoiot;

public class Task {
    private String schedulerName;
    private int cycle;
    private int flow1;
    private int flow2;
    private int flow3;
    private String startTime;
    private String stopTime;
    private boolean isActive;
    private int status;
    private int curCycle;

    public Task(String schedulerName, int cycle, int flow1, int flow2, int flow3, String startTime, String stopTime) {
        this.schedulerName = schedulerName;
        this.cycle = cycle;
        this.flow1 = flow1;
        this.flow2 = flow2;
        this.flow3 = flow3;
        this.startTime = startTime;
        this.stopTime = stopTime;
        this.isActive = true;
    }

    public String getStatus() {
        String curArea = "A";
        if (curCycle % 3 == 1) {
            curArea = "B";
        } else if (curCycle % 3 == 2) {
            curArea = "C";
        }
        switch (this.status) {
            case 0:
                return "IDLE";
            case 1:
                return "MIXER1";
            case 2:
                return "MIXER2";
            case 3:
                return "MIXER2";
            case 4:
                return "PUMP_IN";
            case 5:
                return "SELECTOR (Area " + curArea + ")";
            case 6:
                return "PUMP_OUT";
            case 7:
                return "NEXT_CYCLE";
            default:
                return "END";
        }
    }

    public void setStatus(int status) {
        this.status = status;
    }

    public int getCurCycle() {
        return curCycle;
    }

    public void setCurCycle(int curCycle) {
        this.curCycle = curCycle;
    }

    public String getSchedulerName() {
        return schedulerName;
    }

    public int getCycle() {
        return cycle;
    }

    public int getFlow1() {
        return flow1;
    }

    public int getFlow2() {
        return flow2;
    }

    public int getFlow3() {
        return flow3;
    }

    public String getStartTime() {
        return startTime;
    }

    public String getStopTime() {
        return stopTime;
    }

    public boolean isActive() {
        return isActive;
    }

    public void setActive(boolean active) {
        isActive = active;
    }

    @Override
    public String toString() {
        return "Task{" +
                "schedulerName='" + schedulerName + '\'' +
                ", cycle=" + cycle +
                ", flow1=" + flow1 +
                ", flow2=" + flow2 +
                ", flow3=" + flow3 +
                ", startTime='" + startTime + '\'' +
                ", stopTime='" + stopTime + '\'' +
                ", isActive=" + isActive +
                ", status=" + status +
                ", curCycle=" + curCycle +
                '}';
    }
}
