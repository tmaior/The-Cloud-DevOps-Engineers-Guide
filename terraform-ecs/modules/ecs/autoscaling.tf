resource "aws_security_group" "cluster_security_group" {
  name        = "${var.cluster_name}-cluster-sg"
  description = "Enables internal access"
  vpc_id      = var.network.vpc_id

  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    protocol    = "tcp"
    from_port   = 80
    to_port     = 80
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}


resource "aws_launch_configuration" "as_conf" {
  iam_instance_profile        = aws_iam_instance_profile.instance_profile.id
  image_id                    = data.aws_ami.ecs_ami.image_id
  security_groups             = [aws_security_group.cluster_security_group.id]
  instance_type               = var.auto_scalling.instance_type
  key_name                    = var.auto_scalling.key_name

  root_block_device {
    volume_size = 30
  }

  user_data = <<EOF
    #!/bin/bash
    #====== Install SSM
      yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm
      start amazon-ssm-agent
      chkconfig amazon-ssm-agent on

    echo ECS_CLUSTER=${aws_ecs_cluster.cluster.name} >> /etc/ecs/ecs.config
    echo ECS_INSTANCE_ATTRIBUTES={\"cluster_type\":\"web\"} >> /etc/ecs/ecs.config   

  EOF
  
  lifecycle {
    create_before_destroy = true
    ignore_changes = [
      image_id
    ]
  }
}

resource "aws_autoscaling_group" "autoscaling_group" {
  launch_configuration = aws_launch_configuration.as_conf.name
  min_size             = var.auto_scalling.min_instances
  desired_capacity     = var.auto_scalling.desired_instances
  max_size             = var.auto_scalling.max_instances
  vpc_zone_identifier  = var.network.subnets
  target_group_arns    = [var.aws_lb_target_group_default_arn]

  tag {
    key                 = "Name"
    value               = "${aws_ecs_cluster.cluster.name}"
    propagate_at_launch = true
  }

  lifecycle {
    create_before_destroy = true
  }
}


resource "aws_autoscaling_policy" "scale_up_policy" {
  name                   = "i${aws_ecs_cluster.cluster.name}-scale-up"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 1
  autoscaling_group_name = aws_autoscaling_group.autoscaling_group.name
}

resource "aws_autoscaling_policy" "scale_down_policy" {
  name                   = "i${aws_ecs_cluster.cluster.name}-scale-down"
  scaling_adjustment     = -1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 1
  autoscaling_group_name = aws_autoscaling_group.autoscaling_group.name
}

