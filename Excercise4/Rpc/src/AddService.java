public class AddService implements AddServiceInterface {
    private volatile int index = 1;

    public Double add(Double num1, Double num2) {
        return num1 + num2;
    }
}
