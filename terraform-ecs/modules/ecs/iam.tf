data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ec2_role" {
  name                = "${aws_ecs_cluster.cluster.name}-ec2-role"
  path                = "/"
  assume_role_policy  = data.aws_iam_policy_document.ec2_assume_role.json
  managed_policy_arns = ["arn:aws:iam::aws:policy/AdministratorAccess"]
}

resource "aws_iam_instance_profile" "instance_profile" {
  name = "${aws_ecs_cluster.cluster.name}-instance-profile"
  role = aws_iam_role.ec2_role.name
}