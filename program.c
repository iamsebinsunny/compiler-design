void main(){
    print("Welcome to our C compiler");
    float a = 5.0;
    int b = 10;
    float c = (a+b)*2;
    print(c);
    if(a>b){
        print("Control flow currently inside if loop");
    }else{
        print("Control flow currently inside if loop");
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