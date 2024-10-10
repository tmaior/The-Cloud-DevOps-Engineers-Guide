output "instance_id" {
  description = "ID da instância EC2"
  value       = aws_instance.web_server.id
}

output "public_ip" {
  description = "Endereço IP público da instância EC2"
  value       = aws_instance.web_server.public_ip
}
