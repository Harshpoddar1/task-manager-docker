provider "aws" {
  region = "ap-southeast-2"
}

resource "aws_instance" "lab" {
  ami           = "ami-06259b63260eddc13"
  instance_type = "t3.micro"

  key_name               = "devops-key"
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tags = {
    Name = "task-manager-server"
  }
}

resource "aws_security_group" "web_sg" {
  name = "task-manager-sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

}
