interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
}

function FeatureCard({ icon, title, description }: FeatureCardProps) {
  return (
    <div className="group bg-white p-8 rounded-xl shadow-sm border border-gray-100 text-center transform transition-all duration-300 hover:shadow-lg hover:border-red-100">
      <div className="flex justify-center mb-6 transition-transform duration-300 group-hover:scale-110">
        {icon}
      </div>
      <h4 className="text-xl font-semibold mb-4 text-gray-900">{title}</h4>
      <p className="text-gray-600 leading-relaxed">{description}</p>
    </div>
  );
}

export default FeatureCard;
