void main(){
    print("Welcome to our C compiler");
    int a = 5;
    float b = 10.0;
    float c =  2.0;
    float d = (b+c)*2;
    print(d);
    if(b>c){
        print("Control flow currently inside if loop");
    }else{
        print("Control flow currently outside if loop");
    }
    def add(int x, int y){
        int sum = x + y;
        print("Sum is" + sum);
    }
    add(5,4);
    while(b>c){
        b = b * 10;
    }
}